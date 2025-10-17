from django.shortcuts import render
import requests
from datetime import datetime, timezone
from rest_framework.response import Response
from rest_framework import status
import logging
from rest_framework.views import APIView
from decouple import config

# Create your views here.

logger = logging.getLogger(__name__)

EMAIL = config("Email")
NAME = config("Name")
STACK = config("Stack")

CAT_URL = config("Api_url")
REQUEST_TIMEOUT = config("Timeout", cast=int)

class Userprofile(APIView):
    def get(self, request):
        response_data = {
            'status': "success",
            'user': {
                "email": EMAIL,
                "name": NAME,
                "stack":  STACK
                
            },
            "timestamp" : datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "fact" : ""
            
        }
        try:
            response = requests.get(CAT_URL, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            api_response = response.json()
            api_fact = api_response.get('fact', 'Cats are wonderful pets')
            
            response_data["fact"] = api_fact
        except requests.exceptions.RequestException as e:
            logger.error(f"Cat api failed: {str(e)} ")    
            response_data["fact"] = "cats are greats but api is unreachable"
        except ValueError:
            logger.error("api didnt return as a valid json")
            response_data["fact"] = "cats are still great but api didnt return a valid json"
         
        return Response(response_data, status=status.HTTP_200_OK)    
            
                