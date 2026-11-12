from django.urls import path
from sokolinkapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.blog, name='blog'),
    path('blog-details/', views.blogdetail, name='blog-details'),
    path('service-details/', views.service, name='service-details'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('starter/', views.starter, name='starter'),
    path('contacts/', views.show, name='contacts'),
    path('contacts/<int:contact_id>/edit/', views.edit_contact, name='contact-edit'),
    path('contacts/<int:contact_id>/delete/', views.delete_contact, name='contact-delete'),
]
