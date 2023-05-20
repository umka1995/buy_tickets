from django.shortcuts import render
from mainapp.tasks import send_mail_func
from django.http import HttpResponse

def send_mail_to_all(request):
    send_mail_func.delay()
    return HttpResponse("Sent")

