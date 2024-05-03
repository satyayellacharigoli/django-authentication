from django.contrib import admin
from django.urls import path
from .views import CustomAuthToken, generate_token

urlpatterns = [
    path('v1/login/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('v1/generate-token/', generate_token),
]
