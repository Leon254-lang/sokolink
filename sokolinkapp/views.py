from django.http import request
from django.shortcuts import render
from django.views.generic import detail

# Create your views here.
def error(request):
    return render(request, '404.html')
def index(request):
    return render(request, 'index.html')
def blog(request):
    return render(request, 'blog.html')
def blogdetail(request):
    return render(request, 'blog-details.html')
def service(request):
    return render(request, 'service-details.html')
def portfolio(request):
    return render(request, 'portfolio-details.html')
def starter(request):
    return render(request, 'starter-page.html'   )
