from django.contrib import admin
from django.urls import path
from sokolinkapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('blog/', views.blog, name='blog'),
    path('blog-details/', views.blogdetail, name='blog-details'),
    path('service-details/', views.service, name='service-details'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('starter/', views.starter, name='starter'),

]
