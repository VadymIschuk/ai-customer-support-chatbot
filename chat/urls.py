from django.urls import path
from . import views

urlpatterns = [
    path('message/', views.process_prompt, name='process_prompt'),
]