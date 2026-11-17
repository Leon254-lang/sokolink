from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Contact


class LoginTests(TestCase):
    def test_login_accepts_email_and_redirects_to_index(self):
        response = self.client.post('/', {
            'username': 'market-owner',
            'email': 'owner@example.com',
            'password': 'test-password',
        })
        self.assertRedirects(response, '/login/')

        response = self.client.post('/login/', {
            'email': 'owner@example.com',
            'password': 'test-password',
        })

        self.assertRedirects(response, '/index/')
        self.assertEqual(
            self.client.session['_auth_user_id'],
            str(get_user_model().objects.get(username='market-owner').pk),
        )

    def test_invalid_login_displays_error(self):
        response = self.client.post('/login/', {
            'email': 'unknown@example.com',
            'password': 'wrong-password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid email or password.')

    def test_login_rejects_duplicate_email_addresses(self):
        user_model = get_user_model()
        user_model.objects.create_user(
            username='first-owner',
            email='shared@example.com',
            password='test-password',
        )
        user_model.objects.create_user(
            username='second-owner',
            email='shared@example.com',
            password='test-password',
        )

        response = self.client.post('/login/', {
            'email': 'shared@example.com',
            'password': 'test-password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid email or password.')


class ContactPageTests(TestCase):
    def test_contact_messages_are_staff_only(self):
        response = self.client.get('/contacts/')

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response['Location'])

    def test_staff_can_view_contact_messages(self):
        staff_user = self._create_staff_user()
        self.client.force_login(staff_user)
        Contact.objects.create(
            name='Alex Example',
            phone='555-0100',
            email='alex@example.com',
            subject='Question',
            message='Please call me.',
        )

        response = self.client.get('/contacts/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alex Example')
        self.assertContains(response, 'Please call me.')

    def test_contact_edit_page_is_staff_only(self):
        contact = self._create_contact()

        response = self.client.get(f'/contacts/{contact.id}/edit/')

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response['Location'])

    def test_staff_can_update_contact_message(self):
        staff_user = self._create_staff_user()
        self.client.force_login(staff_user)
        contact = self._create_contact()
        url = f'/contacts/{contact.id}/edit/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="Alex Example"')

        response = self.client.post(url, {
            'name': 'Alex Updated',
            'phone': '555-0199',
            'email': 'updated@example.com',
            'subject': 'Updated question',
            'message': 'An updated message.',
        })

        self.assertRedirects(response, '/contacts/')
        contact.refresh_from_db()
        self.assertEqual(contact.name, 'Alex Updated')
        self.assertEqual(contact.email, 'updated@example.com')
        self.assertEqual(contact.message, 'An updated message.')

    def test_invalid_contact_edit_keeps_existing_record(self):
        staff_user = self._create_staff_user()
        self.client.force_login(staff_user)
        contact = self._create_contact()

        response = self.client.post(f'/contacts/{contact.id}/edit/', {
            'name': 'Alex Updated',
            'phone': '555-0199',
            'email': 'not-an-email',
            'subject': 'Updated question',
            'message': 'An updated message.',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Review the highlighted fields and try again.')
        contact.refresh_from_db()
        self.assertEqual(contact.name, 'Alex Example')
        self.assertEqual(contact.email, 'alex@example.com')

    def test_empty_contact_edit_shows_required_field_errors(self):
        staff_user = self._create_staff_user()
        self.client.force_login(staff_user)
        contact = self._create_contact()

        response = self.client.post(f'/contacts/{contact.id}/edit/', {})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')
        contact.refresh_from_db()
        self.assertEqual(contact.name, 'Alex Example')

    def test_contact_form_saves_valid_submission(self):
        response = self.client.post('/', {
            'name': 'Alex Example',
            'phone': '555-0100',
            'email': 'alex@example.com',
            'subject': 'Question',
            'message': 'Please call me.',
        })

        self.assertRedirects(response, '/')
        self.assertTrue(Contact.objects.filter(email='alex@example.com').exists())

    def test_contact_form_displays_validation_errors(self):
        response = self.client.post('/', {
            'name': 'Alex Example',
            'phone': '555-0100',
            'email': 'not-an-email',
            'subject': 'Question',
            'message': 'Please call me.',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please correct the errors below and try again.')
        self.assertEqual(Contact.objects.count(), 0)

    def test_staff_can_delete_a_contact_with_post(self):
        staff_user = self._create_staff_user()
        self.client.force_login(staff_user)
        contact = Contact.objects.create(
            name='Alex Example',
            phone='555-0100',
            email='alex@example.com',
            subject='Question',
            message='Please call me.',
        )

        response = self.client.post(f'/contacts/{contact.id}/delete/')

        self.assertRedirects(response, '/contacts/')
        self.assertFalse(Contact.objects.filter(pk=contact.id).exists())

    def test_contact_delete_rejects_get(self):
        staff_user = self._create_staff_user()
        self.client.force_login(staff_user)
        contact = Contact.objects.create(
            name='Alex Example',
            phone='555-0100',
            email='alex@example.com',
            subject='Question',
            message='Please call me.',
        )

        response = self.client.get(f'/contacts/{contact.id}/delete/')

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Contact.objects.filter(pk=contact.id).exists())

    def _create_staff_user(self):
        from django.contrib.auth import get_user_model

        return get_user_model().objects.create_user(
            username='staff',
            password='test-password',
            is_staff=True,
        )

    def _create_contact(self):
        return Contact.objects.create(
            name='Alex Example',
            phone='555-0100',
            email='alex@example.com',
            subject='Question',
            message='Please call me.',
        )
