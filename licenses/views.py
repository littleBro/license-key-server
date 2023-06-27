import json
from datetime import datetime

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .models import LicenseKey
import base64


def _load_private_key():
    # Load the private key from a file
    with open("pki/private_key.pem", "rb") as key_file:
        return serialization.load_pem_private_key(key_file.read(), password=None)


def _sign_message(private_key, message):
    signature = private_key.sign(
        message.encode(),
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    # We'll base64 encode the signature so that it's safe to include in our JSON response
    return base64.b64encode(signature).decode()


def validate_license_key(request):
    license_key = request.GET.get('key', None)
    if license_key is None:
        return JsonResponse({'error': 'Missing "key" parameter'}, status=400)

    try:
        license_key = LicenseKey.objects.get(key=license_key)
        valid = {'valid': license_key.is_active, 'key': str(license_key), 'timestamp': str(datetime.now())}
        private_key = _load_private_key()
        signature = _sign_message(private_key, json.dumps(valid))
        return JsonResponse({'valid': license_key.is_active, 'signature': signature, 'timestamp': valid['timestamp']})

    except ValidationError:
        return JsonResponse({'valid': False, 'signature': '', 'timestamp': ''}, status=400)

    except LicenseKey.DoesNotExist:
        return JsonResponse({'valid': False, 'signature': '', 'timestamp': ''})
