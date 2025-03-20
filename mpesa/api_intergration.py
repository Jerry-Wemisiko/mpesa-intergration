import requests, base64, json, time
from django.conf import settings
from requests.auth import HTTPBasicAuth
from datetime import datetime
from .models import MpesaAccessToken

def get_mpesa_token():
    """
     Fetches an access token from the database if valid, otherwise requests a new one from M-Pesa.
    """
  
# 1️⃣ Check if we already have a valid token in the database
    token_entry = MpesaAccessToken.objects.first()
    
    if token_entry and token_entry.is_token_valid():
        return token_entry.token  # Return existing valid token
    # 2️⃣ If no valid token, request a new one
    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(
        auth_url,
        auth=HTTPBasicAuth(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET),
    )
    response_data = response.json()
    
    if "access_token" in response_data:
        new_token = response_data["access_token"]
        new_token_expiry_time = time.time() + 3600
        
    
        # 3️⃣ Save the new token in the database
        MpesaAccessToken.objects.all().delete()  # Delete existing token
        MpesaAccessToken.objects.create(token=new_token, expiry_time=new_token_expiry_time)
        return new_token    

    else:
        
        raise Exception(f"Could not get M-Pesa access token :{response_data}")
    
    

def register_mpesa_urls():
    """
    Registers the validation and confirmation URLs for M-Pesa transactions.
    Required for receiving payment notifications.
    """
    mpesa_token = get_mpesa_token()

    payload = {
        "ShortCode": settings.MPESA_SHORTCODE,
        "ResponseType": "Completed",
        "ConfirmationURL": f"{settings.NGROK_URL}/confirmation",
        "ValidationURL": f"{settings.NGROK_URL}/validation",
    }

    response = requests.post(
        "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl",
        json=payload,
        headers={
            "Authorization": f"Bearer {mpesa_token}",  # Corrected variable
            "Content-Type": "application/json",
        },
    )
    return response.json()

def lipa_na_mpesa(phone_number, amount):
    """
    Initiates a Lipa na M-Pesa STK Push (Sim Toolkit prompt).
    The user will receive a prompt on their phone to enter their PIN and pay.
    """
    access_token = get_mpesa_token()  # Corrected function call
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    password = base64.b64encode(
        f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}".encode()
    ).decode("utf-8")

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": settings.CALLBACK_URL,
        "AccountReference": "TEST",
        "TransactionDesc": "Payment for services",
    }

    response = requests.post(
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
    )

    return response.json()
