import requests
from django.shortcuts import redirect
import os
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

def root_redirect_view(request):
    """ Redirect to the /me endpoint """
    return redirect('me-view')


""" Create your views here.
APIView for the /me endpoint that retrieves user profile information from an external API.
"""
class MeView(APIView):
    
    #step1: Fetch Cat fact from the external API
    def get(self, request, *args, **kwargs):
        
        #Handle GET request to fetch cat fact
        cat_fact = "Cat fact is unavailable for now. Please try again"

        try:
            cat_fact_response = requests.get('https://catfact.ninja/fact', timeout=5)
            cat_fact_response.raise_for_status()
            cat_fact_data = cat_fact_response.json()
            cat_fact = cat_fact_data.get("fact", cat_fact)

        except requests.exceptions.RequestException:
            cat_fact = "Could not retrieve a cat fact at this time. Please try again"
    # Step2: Generate timestamp
        current_timestamp = datetime.datetime.utcnow().isoformat() + 'Z'

    # Step3: Retrieve user information 
        user_data = {
            'email': os.getenv('MY_EMAIL', 'victorcourage1@gmail.com'),
            'name': os.getenv('MY_NAME', 'Anuonye Chidera'),
            'stack': os.getenv('MY_STACK', 'Python/Django Developer')
    }

    # Step4: Construct the response data
        response_data = {
            'status': 'success',
            'user': user_data,
            'timestamp': current_timestamp,
            'fact': cat_fact
    }
        return Response(response_data, status=status.HTTP_200_OK)
