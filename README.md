# Envoy2ChargeHQ

Based of pgroom / ChargeHQ Git. Modfications required for newer envoy systems. 

Python script first generates a session ID with the bearer token. Then makes an API Call to grab curent data via a Json file and compiles it into a format that Charge HQ can injest.

API called based on the Envoy documentation avaliable here: https://enphase.com/download/accessing-iq-gateway-local-apis-or-local-ui-token-based-authentication

crontab to run every minute, 5AM to 10PM daily;  */1 5-21 * * * <path>/chargehq.py


POST's the following json to ChargeHQ;
{"apiKey": "not_telling", "siteMeters": {"production_kw": 0.00, "net_import_kw": 0.00, "consumption_kw": 0.00}}

Negative net_import = exporting
