import requests, base64, json, os
import time
from django.conf import settings
from requests.auth import HTTPBasicAuth
from datetime import datetime

mpesa_token =None
token_expiry_time = 0


def get_access_token():
    global mpesa_token, token_expiry_time
    
    if mpesa_token and token_expiry_time < token_expiry_time:
        return mpesa_token
    
    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(
        auth_url,
        auth=HTTPBasicAuth(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET),
    )
    
    response_data = response.json()
    if response_data.get("access_token"):
        mpesa_token = response_data["access_token"]
        token_expiry_time = time.time() + 3600
        return mpesa_token
    else:
        raise Exception("Could not get mpesa access token")

def register_mpesa_urls():
    access_token = get_access_token()
    
    payload = {
        "ShortCode": settings.MPESA_SHORTCODE,
        "ResponseType": "Completed",
        "ConfirmationURL": f"{settings.NGROK_URL}/confirmation",
        "ValidationURL": f"{settings.NGROK_URL}/validation",
    }
    response =requests.post("https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl",
        json=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        )
    return response.json()
    
    


def lipa_na_mpesa(phone_number):
    access_token = get_access_token()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(
        f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}".encode()
    ).decode("utf-8")

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": settings.CALLBACK_URL,
        "AccountReference": "tEST",
        "TransactionDesc": "payd",
    }
    response = requests.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },   
    ) 

    return response.json()