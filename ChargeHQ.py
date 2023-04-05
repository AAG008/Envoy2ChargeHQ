#!/usr/bin/env python3

import urllib.request
import json
import requests
import logging
import ssl
import urllib3
from config import *
from socket import timeout
from urllib.error import HTTPError, URLError

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


error = 'None'

# Create SSL context and load certificate file
context = ssl.create_default_context()
context.load_verify_locations('yourenvoycert.crt')

session = requests.Session()
headers = {'Authorization': f'Bearer {token}'}
response = session.get(unlock, headers=headers)
cookies = response.cookies

# Extract session ID from response cookies
session_id = cookies.get('sessionId')

# Grab local Envoy production json
try:
    headers = {'Authorization':f'Bearer {token}', 'Cookie': f'SESSIONID={session_id}'}
    req = urllib.request.Request(source, headers=headers, method='GET')
    with urllib.request.urlopen(req, timeout=5, context=context) as url:
        data = json.loads(url.read().decode())

except HTTPError as e:
    error = f'HTTPError: {e.code}'
    print(error)
    print(headers)

except URLError as e:
    error = f'URLError: {e.reason}'
    print(error)
    print(headers)
except timeout:
    error = 'Timeout'
    print(error)
except Exception as e:
    error = f'Error: {e}'
    print(error)
    print(headers)

else:
    # Massage Envoy json into ChargeHQ compatible json
    consumption = round(data['meters']['load']['agg_p_mw'] / 1000000, 2)
    production = round(data['meters']['pv']['agg_p_mw'] / 1000000, 2)
    grid = round(production - consumption, 2)

    if grid < 0:
        grid = abs(grid)  # Invert grid value from Envoy value to keep ChargeHQ happy
    else:
        grid = -abs(grid)  # Invert grid value from Envoy value to keep ChargeHQ happy

    # create new json
    jsondata = {}
    jsondata['apiKey'] = apiKey
    jsondata['siteMeters'] = {}
    jsondata['siteMeters']['production_kw'] = production
    jsondata['siteMeters']['net_import_kw'] = grid
    jsondata['siteMeters']['consumption_kw'] = consumption 
    json_dump = json.dumps(jsondata)

    # POST json to ChargeHQ
    header = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(endPoint, data=json_dump, headers=header)
    print(f"Status Code: {r.status_code}, Response: {r.json()}")
