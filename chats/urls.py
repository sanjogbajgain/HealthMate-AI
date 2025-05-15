from django.urls import path
from . import views

urlpatterns = [
    path('post_message/', views.post_message, name='post_message'),
    path('get_messages/', views.get_messages, name='get_messages'),
    path('post_feedback/', views.post_feedback, name='post_feedback'),
    path('get_feedback/', views.get_feedback, name='get_feedback'),
    
]
