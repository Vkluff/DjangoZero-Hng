from django.urls import path
from .views import MeView, root_redirect_view

urlpatterns = [
    path('me/', MeView.as_view(), name='me-view'), 
    path('', root_redirect_view, name='root-redirect'), 
]
