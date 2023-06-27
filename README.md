# License Key Management Server

### Installation

1. Create a `.env` file in the root directory:
```
# Fill this with a long random string
DJANGO_SECRET_KEY='some-long-random-secret-string'

# Your domain, IP or 127.0.0.1
HOST='your-server-domain.com'

# The port for application
PORT=8000
```

2. Build the project using Docker Compose:
```
docker-compose build
```

3. Run the server:
```
docker-compose up -d
```

4. Apply initial DB migrations:
```
docker-compose exec app python manage.py migrate
```

5. Create a superuser for the admin panel:
```
docker-compose exec app python manage.py createsuperuser
```

You can now access the application at the chosen host and port, e.g. `http://127.0.0.1:8000/admin`.

### Generating keys

You will need to generate a private-public key pair for signing and verifying responses. Run the following Django command:
```
docker-compose exec app python manage.py generate_pki
```

This will generate a private key and a public key in the `pki` directory. The private key will be used by the server for signing responses, and the public key will be used by the client to verify the signature.


## API

The server provides an endpoint for validating license keys:

`GET /licenses/validate?key=<key>`

This will return a JSON response containing whether the key is valid or not, a timestamp, and a signature.


## Client-Side Example

The following Python script demonstrates how a client might interact with the license validation API:

```python
import requests
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
import base64


def load_public_key():
    with open("pki/public_key.pem", "rb") as key_file:
        return serialization.load_pem_public_key(key_file.read())

    
def verify_signature(public_key, signature, message):
    signature = base64.b64decode(signature)
    try:
        public_key.verify(
            signature,
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), 
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False

def check_license(server_url, license_key):
    response = requests.get(server_url + "/licenses/validate", params={'key': license_key})
    data = response.json()
    public_key = load_public_key()
    valid = verify_signature(
        public_key, 
        data['signature'], 
        json.dumps({'valid': data['valid'], 'key': license_key, 'timestamp': data['timestamp']}))
    return valid

server_url = "<your-server-url>"
license_key = "<your-license-key>"
is_valid = check_license(server_url, license_key)
if is_valid:
    print("License is valid.")
else:
    print("License is invalid or has been tampered with.")
```
