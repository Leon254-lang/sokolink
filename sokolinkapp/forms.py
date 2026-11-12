from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'phone', 'email', 'subject', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name-field'}),
            'phone': forms.TelInput(attrs={'class': 'form-control', 'id': 'phone-field'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email-field'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'id': 'subject-field'}),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'message-field',
                'rows': 10,
            }),
        }
