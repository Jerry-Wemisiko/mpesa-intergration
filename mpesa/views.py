import json
import requests
from requests.auth import HTTPBasicAuth
from django.http import  JsonResponse
from django.conf import settings
from .api_intergration import get_access_token, lipa_na_mpesa

# Create your views here.



def mpesa_payd_view(request):
    phone_number = "2547462123493"
    amount = 300000000
    
    data = lipa_na_mpesa(phone_number, amount)  
    
    return JsonResponse(data)

