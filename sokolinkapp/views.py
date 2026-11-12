from django.contrib import messages
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


@staff_member_required
def show(request):
    contacts = Contact.objects.order_by('-id')
    return render(request, 'show.html', {'contacts': contacts})


@staff_member_required
@require_POST
def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    contact.delete()
    messages.success(request, 'The contact message was deleted.')
    return redirect('contacts')