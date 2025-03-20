from django.shortcuts import render
import requests
from django.http import  JsonResponse
from django.conf import settings
from .api_intergration import get_access_token, lipa_na_mpesa

# Create your views here.

# def fetch_mpesa_data(request):
    
#     access_token = get_access_token()
#     if not access_token :
#         return JsonResponse({"error": "Failed to get access token"},status=500)

#     transaction_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
#     headers={
#         "Authorization": f"Bearer{access_token}",
#         "Content-Type":"application/json"
#     }
#     payload = {
#         "BusinessShortCode": settings.MPESA_SHORTCODE,
#         "Password": password,
#         "Timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
#         "TransactionType": "CustomerPayBillOnline", 
#         "Amount": 1,
#     }

def mpesa_payd_view(request):
    phone_number = "2547462123493"
    amount = 300000000
    
    data = lipa_na_mpesa(phone_number, amount)  
    
    return JsonResponse(data)

