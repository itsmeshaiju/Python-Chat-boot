from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('list/',views.list),
    path('generate_content/',views.generate_content),
    path('chat/', views.chat_view, name='chat_view'),
]