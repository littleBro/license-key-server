import os

from django.core.management.base import BaseCommand
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


class Command(BaseCommand):
    help = 'Generates a private and public key pair for RSA encryption'

    def handle(self, *args, **options):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        public_key = private_key.public_key()

        os.makedirs('pki', exist_ok=True)

        # Save the private key to a file
        with open('pki/private_key.pem', 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        # Save the public key to a file
        with open('pki/public_key.pem', 'wb') as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

        self.stdout.write(self.style.SUCCESS('Successfully generated key pair'))
