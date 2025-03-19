from django.http import HttpResponse
from django.contrib import admin
from django.urls import path

def homepage(request):
    return HttpResponse("Get paid with Mpesa")
urlpatterns = [
    path("", homepage),
]
