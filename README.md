Envoy2chargehq

Based on pgroom/ChargeHQ Git, modifications are required for newer Envoy systems.

The Python script first generates a session ID with the bearer token. Then it makes an API call to grab current data via a JSON file and compiles it into a format that Charge HQ can ingest.

The API call is based on the Envoy documentation available here: https://enphase.com/download/accessing-iq-gateway-local-apis-or-local-ui-token-based-authentication

Crontab should be set to run every minute, 5 AM to 10 PM daily: */1 5-21 * * * /chargehq.py

The following JSON is POSTed to ChargeHQ: {"apiKey": "not_telling", "siteMeters": {"production_kw": 0.00, "net_import_kw": 0.00, "consumption_kw": 0.00}}

Negative net_import = exporting

On 6/04/23, values were reporting incorrectly. Investigating cause. #update# Wrong value was being pulled from the JSON file. It was corrected to PV, and the value had to be divided by three extra zeros, as the decimal point is not in this version of the API call.

It is recommended to run the script on a Linux system that is on during daylight hours. Make sure that Python3 or higher is installed.

Steps for usage:

Populate your details in the generatetoken.py.
Run generate that token. Copy that token down.
Populate all details in the config.py.
Manually run the chargehq.py to ensure that the script runs correctly without error.
Place the script in crontab to run every minute.
Possible issues: because the web service is presenting a self-signed certificate, it may present an error. You can install the certificate by grabbing it from the web page and importing this cert into the Python trusted store. You can disable SSL verification in Python. You can add a host entry to match the SSL cert's CN.

17/04/23, Minor updates to production URL and data called. Reverted back to the old URL, was getting inconsistant Data feed from the document API.
