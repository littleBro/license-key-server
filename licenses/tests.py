from django.test import TestCase
from django.urls import reverse
from .models import LicenseKey
from uuid import uuid4
import base64
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


class LicenseServerTests(TestCase):

    def setUp(self):
        self.license_key = LicenseKey.objects.create(employee_name="Test", is_active=True)
        self.inactive_license_key = LicenseKey.objects.create(employee_name="Test", is_active=False)
        self.validation_url = reverse('validate_license_key')
        # Load the public key from a file
        with open("pki/public_key.pem", "rb") as key_file:
            self.public_key = serialization.load_pem_public_key(key_file.read())

    def test_license_key_validation(self):
        response = self.client.get(self.validation_url, {'key': str(self.license_key.key)})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['valid'])

        # Verify the signature
        signature = base64.b64decode(data['signature'])
        valid = {'valid': data['valid'], 'key': str(self.license_key.key), 'timestamp': data['timestamp']}
        message = json.dumps(valid).encode()
        self.public_key.verify(
            signature,
            message,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )

    def test_invalid_key(self):
        response = self.client.get(self.validation_url, {'key': 'invalid_key'})
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['valid'])

    def test_no_key(self):
        response = self.client.get(self.validation_url)
        self.assertEqual(response.status_code, 400)

    def test_non_existent_key(self):
        response = self.client.get(self.validation_url, {'key': str(uuid4())})  # non-existent key
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['valid'])

    def test_inactive_key(self):
        response = self.client.get(self.validation_url, {'key': str(self.inactive_license_key.key)})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['valid'])
