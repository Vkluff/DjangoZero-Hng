
# Dynamic Profile Endpoint with Django REST Framework

## Introduction

As part of a backend internship track with HNG-TECH, I was tasked with building a simple RESTful API endpoint that returns my profile information that also fetched a random cat fact from an external API dynamically.

This was a straightforward task on how to structure clean JSON responses, and how to handle real-world reliability issues like failed external requests.

This post documents my process, challenges, and lessons learned. 🧠

## 🧩 The Task Breakdown

The main goal was to build a single endpoint:

```
GET /api/me
```

which returns a JSON response in this structure:

```json
{
  "status": "success",
  "user": {
    "email": "your_email@example.com",
    "name": "Your Full Name",
    "stack": "Python/Django"
  },
  "timestamp": "2025-10-17T13:42:56.789Z",
  "fact": "Cats sleep for 70% of their lives."
}
```

**Key requirements:**
- Return the current UTC time in ISO 8601 format
- Fetch a random cat fact from https://catfact.ninja/fact
- Handle potential API or network errors
- Follow REST best practices and return Content-Type: application/json

## ⚙️ Step 1: Setting Up Django

I started by creating a virtual environment and installing the necessary packages:

```bash
pip install django djangorestframework requests python-dotenv
```

Then I built the app structure:

```
myproject/
│
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── profile_api/
│   ├── __init__.py
│   ├── views.py
│   ├── urls.py
│   └── serializers.py
└── .env
```

## 🧠 Step 2: Writing the API Logic

In `profile_api/views.py`:

```python
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

```

In `profile_api/urls.py`:

```python
from django.urls import path
from .views import MeView, root_redirect_view

urlpatterns = [
    path('me/', MeView.as_view(), name='me-view'), 
    path('', root_redirect_view, name='root-redirect'), 
]

```

This code does a few key things:
- Fetches live data from an external API
- Returns a clean, consistent JSON response
- Gracefully handles API failure with a fallback message
- Dynamically updates the timestamp on every request

## 🚀 Step 3: Running the Project

### Environment Setup

Create a `.env` file in your project root:

```env
MY_EMAIL=your.email@example.com
MY_NAME=Your Full Name
MY_STACK=Python/Django
```

### Run the Development Server

```bash
# Activate virtual environment
source .venv/bin/activate

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/api/me/` to test your API endpoint.

## 📦 Dependencies

Create a `requirements.txt` file:

```txt
Django==5.2.7
djangorestframework==3.15.2
requests==2.31.0
python-dotenv==1.0.0
```

Install with:
```bash
pip install -r Requirements.txt
```

## 🎯 Key Features

- **Clean JSON Responses**: Structured output following REST best practices
- **Error Handling**: Graceful fallback when external API fails
- **Environment Configuration**: Secure management of sensitive data
- **UTC Timestamp**: Accurate ISO 8601 formatted timestamps
- **External API Integration**: Dynamic cat facts from catfact.ninja

## 🔧 API Response Example

```json
{
  "status": "success",
  "user": {
    "email": "victorcourage1@gmail.com",
    "name": "Anuonye Chidera",
    "stack": "Python/Django"
  },
  "timestamp": "2025-10-18T15:34:22.123456Z",
  "fact": "A group of cats is called a clowder."
}
```

## 💡 Lessons Learned

- **Error handling is crucial** when depending on external APIs
- **Environment variables** keep sensitive data secure
- **Django REST Framework** makes building APIs straightforward
- **Proper timestamp formatting** ensures compatibility across systems
