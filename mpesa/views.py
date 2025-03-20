import json
import requests
from requests.auth import HTTPBasicAuth
from django.http import  JsonResponse
from django.conf import settings
from .api_intergration import get_access_token, lipa_na_mpesa,register_mpesa_urls

# Create your views here.
def homepage(request):
    data = {
        "message": "Get paid with Mpesa",
        "status": "success"
    }
    return JsonResponse(data)


def get_access_token_view(request):
    """
    View to get the access token from the M-Pesa API and display it as JSON."""
    token_data = get_access_token()
    return JsonResponse({"token_data": token_data})

def register_mpesa_urls_view(request):
    """
    View to register the mpesa urls(validation and confirmation URLs) for M-Pesa transactions and display it as JSON.
    """
    resp_data= register_mpesa_urls()
    return JsonResponse(resp_data)
                        
def mpesa_payd_view(request):
    """
    View to initiate a Lipa na M-Pesa transaction.
    Example: http://127.0.0.1:8000/lipa-na-mpesa/?phone=254712345678&amount=100
    """
    
    phone_number = request.GET.get("phone", "254708374149")  # Use sandbox test number by default
    amount = request.GET.get("amount", 100)  # Default to 100 if no amount is provided
    
    try:
        amount = int(amount)  # Ensure amount is an integer
    except ValueError:
        return JsonResponse({"error": "Amount must be a valid number"}, status=400)

 # Use sandbox test credentials
    if phone_number != "254708374149":
        return JsonResponse({"error": "Use the sandbox test phone number"}, status=400)

    data = lipa_na_mpesa(phone_number, amount)  
    
    return JsonResponse(data)

