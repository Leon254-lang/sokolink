from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login as auth_login
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ContactForm
from .models import Contact


def error(request):
    return render(request, '404.html')


def index(request):
    contact_form = ContactForm(request.POST or None)
    if request.method == 'POST':
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, 'Your message has been received. Thank you!')
            return redirect('index')

    return render(request, 'index.html', {'contact_form': contact_form})


def blog(request):
    return render(request, 'blog.html')


def blogdetail(request):
    return render(request, 'blog-details.html')


def service(request):
    return render(request, 'service-details.html')


def portfolio(request):
    return render(request, 'portfolio-details.html')


def starter(request):
    return render(request, 'starter-page.html')
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Here you can add logic to create a new user or perform any other actions
        # For example, you can use Django's User model to create a new user
        from django.contrib.auth.models import User
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('login')

    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = (request.POST.get('email') or '').strip()
        password = request.POST.get('password')

        # Authenticate the user based on email and password
        matching_users = (
            list(get_user_model().objects.filter(email__iexact=email)[:2])
            if email and password else []
        )
        user = None
        if len(matching_users) == 1:
            user = authenticate(
                request,
                username=matching_users[0].get_username(),
                password=password,
            )

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('index')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')    


@staff_member_required
def show(request):
    contacts = Contact.objects.order_by('-id')
    return render(request, 'show.html', {'contacts': contacts})


@staff_member_required
def edit_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    contact_form = ContactForm(
        request.POST if request.method == 'POST' else None,
        instance=contact,
    )

    if request.method == 'POST' and contact_form.is_valid():
        contact_form.save()
        messages.success(request, 'The contact message was updated.')
        return redirect('contacts')

    return render(request, 'edit.html', {
        'contact': contact,
        'contact_form': contact_form,
    })


@staff_member_required
@require_POST
def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    contact.delete()
    messages.success(request, 'The contact message was deleted.')
    return redirect('contacts')