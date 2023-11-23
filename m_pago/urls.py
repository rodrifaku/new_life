from .views import mail
from django.urls import path

urlpatterns = [
    path('mail', mail, name='mail'),
]

