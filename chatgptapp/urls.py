from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [

   
    path('',views.generate_content, name='generate_content'),
    path('download_as_pdf/', views.download_as_pdf, name='download_as_pdf'),

]
