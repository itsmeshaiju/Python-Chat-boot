from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('generate_content/',views.generate_content, name='generate_content'),
    path('logout/', views.logout, name='logout'),
    path('download_as_pdf/', views.download_as_pdf, name='download_as_pdf'),

]
