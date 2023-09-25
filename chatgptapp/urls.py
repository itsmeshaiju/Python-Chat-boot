from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [

   
    path('',views.generate_content, name='generate_content'),
    path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('download_as_pdf/', views.download_as_pdf, name='download_as_pdf'),

]
