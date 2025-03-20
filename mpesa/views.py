import json
import requests
from django.http import JsonResponse
from django.conf import settings
from .api_intergration import get_mpesa_token, lipa_na_mpesa, register_mpesa_urls

# Create your views here.
def homepage(request):
    return JsonResponse({
        "message": "Get paid with Mpesa",
        "status": "success"
    })


def get_access_token_view(request):
    """
    View to get the access token from the M-Pesa API and display it as JSON.
    """
    token_data = get_mpesa_token()  
    return JsonResponse({"access_token": token_data})


def register_mpesa_urls_view(request):
    """
    View to register the M-Pesa URLs (validation and confirmation URLs) and display the response as JSON.
    """
    response_data = register_mpesa_urls()
    return JsonResponse(response_data)


def mpesa_payd_view(request):
    """
    View to initiate a Lipa na M-Pesa transaction.
    Example: http://127.0.0.1:8000/lipa-na-mpesa/?phone=254708374149&amount=100
    """
    phone_number = request.GET.get("phone", "254708374149")  
    amount = request.GET.get("amount", 100)  

    try:
        amount = int(amount)  # Ensure amount is an integer
    except ValueError:
        return JsonResponse({"error": "Amount must be a valid number"}, status=400)

    # Enforce test phone number in the sandbox
    if phone_number != "254708374149":
        return JsonResponse({"error": "Use the sandbox test phone number: 254708374149"}, status=400)

    response_data = lipa_na_mpesa(phone_number, amount)

    return JsonResponse(response_data)
