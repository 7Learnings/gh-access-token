import time
import os
import sys
import subprocess
import json
import base64
import tempfile
import typing
from pprint import pprint
from urllib.request import Request, urlopen


GITHUB_APP_PRIVATE_KEY = os.environ['APP_PRIVATE_KEY']
GITHUB_APP_IDENTIFIER = 124662
GITHUB_INSTALLATION_ID = 18015726

# https://jwt.io/introduction
def b64(b: typing.Union[str, bytes]) -> str:
    if isinstance(b, str):
        b = b.encode()
    return base64.urlsafe_b64encode(b).decode().rstrip('=')

# https://stackoverflow.com/a/62646786/2371032
now = int(time.time())
expiration = 300
header=dict(alg='RS256')
payload = dict(iat=now, exp=now + expiration, iss=GITHUB_APP_IDENTIFIER)
enc=f"{b64(json.dumps(header))}.{b64(json.dumps(payload))}"
with tempfile.NamedTemporaryFile('w') as pem, tempfile.NamedTemporaryFile('w') as t:
    pem.write(GITHUB_APP_PRIVATE_KEY)
    pem.flush()
    t.write(enc)
    t.flush()
    signature = b64(subprocess.check_output(['openssl', 'dgst', '-sha256', '-sign', pem.name, t.name]))

jwt = f"{enc}.{signature}"

resp = json.loads(urlopen(Request(f"https://api.github.com/app/installations/{GITHUB_INSTALLATION_ID}/access_tokens", headers=dict(Authorization=f"Bearer {jwt}"), method='POST')).read().decode())
pprint(resp, stream=sys.stderr)
print(resp['token'])
