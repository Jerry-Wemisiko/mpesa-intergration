from django.http import JsonResponse
from django.contrib import admin
from django.urls import path , include

def homepage(request):
    data = {
        "message": "Get paid with Mpesa",
        "status": "success"
    }
    return JsonResponse(data)

# urlpatterns = [
#     path("", homepage),
# ]
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("mpesa.urls")),  # Include mpesa URLs
]