import requests, base64, json, os
import time
from django.conf import settings
from requests.auth import HTTPBasicAuth
from datetime import datetime

# Global variables to store the access token and its expiry time
mpesa_token =None
token_expiry_time = 0


def get_access_token():
    """
    Fetches an access token from the Safaricom M-Pesa API.
    The token is stored globally and reused until it expires.
    """
    global mpesa_token, token_expiry_time
    
    if mpesa_token and time.time() < token_expiry_time:
        return mpesa_token
    
    # Endpoint for getting the access/auth token

    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    # Make the request with authentication

    response = requests.get(
        auth_url,
        auth=HTTPBasicAuth(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET),
    )
    
    # Convert the response to JSON
   
    response_data = response.json()
    
    # If the response contains an access token, store it

    if response_data.get("access_token"):
        mpesa_token = response_data["access_token"]
        token_expiry_time = time.time() + 3600
        return mpesa_token
    else:
        raise Exception("Could not get mpesa access token")

def register_mpesa_urls():
    """
    Registers the validation and confirmation URLs for M-Pesa transactions.
    Required for receiving payment notifications.
    """
    access_token = get_access_token()
    
    # Define the payload (data) to send

    payload = {
        "ShortCode": settings.MPESA_SHORTCODE,
        "ResponseType": "Completed",
        "ConfirmationURL": f"{settings.NGROK_URL}/confirmation",
        "ValidationURL": f"{settings.NGROK_URL}/validation",
    }
    
    # Make the API request

    response =requests.post("https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl",
        json=payload,  # Send data as JSON
        headers={
            "Authorization": f"Bearer {access_token}",  # Attach token for authentication
            "Content-Type": "application/json",
        },
        )
    return response.json()  # Return the response as JSON
    
    


def lipa_na_mpesa(phone_number):
    """
    Initiates a Lipa na M-Pesa STK Push (Sim Toolkit prompt).
    The user will receive a prompt on their phone to enter their PIN and pay.
    """    
    access_token = get_access_token()  # Get the access token
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # Generate a timestamp
    password = base64.b64encode(
        f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}".encode()
    ).decode("utf-8")  # Encode the password for authentication

    # Define the payload (request body)

    payload = {
 "BusinessShortCode": settings.MPESA_SHORTCODE,  # Your business shortcode
        "Password": password,  # Encoded password
        "Timestamp": timestamp,  # Timestamp
        "TransactionType": "CustomerPayBillOnline",  # Transaction type
        "Amount": amount,  # Amount to charge the customer
        "PartyA": phone_number,  # Customer's phone number
        "PartyB": settings.MPESA_SHORTCODE,  # Business shortcode (Paybill)
        "PhoneNumber": phone_number,  # Same as PartyA
        "CallBackURL": settings.CALLBACK_URL,# Where to send payment results
        "AccountReference": "tEST",# Reference name (used in business records)
        "TransactionDesc": "payd",
    }
    
    # Make the API request

    response = requests.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        json=payload,  # Send data as JSON
        headers={
            "Authorization": f"Bearer {access_token}",  # Attach token
            "Content-Type": "application/json",
        },   
    ) 

    return response.json()  # Return the response as JSON
