from django.urls import path
from .views import validate_license_key

urlpatterns = [
    path('validate/', validate_license_key, name='validate_license_key'),
]
