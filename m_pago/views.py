from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings


def send_email(mail):
    print(mail)

def mail(request):
    if request.method=='POST':
        mail.request.POST.get('mail')    
        send_email(email)
    return HttpResponse('mail sent successfully')
    return render(request, 'negocio/mail.html',{})

def email(request):
    send_mail(
        "Subject here",
        "Here is the message.",
        settings.EMAIL_HOST_USER,
        ["rfaundez.rodrigo@gmail.com"],
        fail_silently=False,
    )
    return HttpResponse('mail sent successfully')

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

