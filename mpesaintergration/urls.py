from django.http import JsonResponse
from django.contrib import admin
from django.urls import path

def homepage(request):
    data = {
        "message": "Get paid with Mpesa",
        "status": "success"
    }
    return JsonResponse(data)

urlpatterns = [
    path("", homepage),
]
