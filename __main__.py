import time
import os
import jwt

GITHUB_APP_PRIVATE_KEY = os.environ['APP_PRIVATE_KEY']
GITHUB_APP_IDENTIFIER = 124662

now = int(time.time())
expiration = 300
payload = dict(iat=now, exp=now + expiration, iss=GITHUB_APP_IDENTIFIER)
encrypted = jwt.encode(payload, key=GITHUB_APP_PRIVATE_KEY, algorithm='RS256')

if isinstance(encrypted, bytes):
    encrypted = encrypted.decode("utf-8")

print(encrypted)
