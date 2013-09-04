"""This module contains the ipvAuth class, which handles authentications"""
import ipviking_api_python.helpers.constants as ipv_consts
from ipviking_django.models import ipvAuthorizer, ValidResponse

APIKEY = ipv_consts.SANDBOX_APIKEY
PROXY = ipv_consts.PROXIES['SANDBOX']    
IPV_AUTH = ipvAuthorizer().configure({'apikey':APIKEY, 'proxy':PROXY})

def configure(authview = None, config = None, rules = None, responses = None):
    """This is the method called externally. Pass it a config dict, a list of IPV_Rule objects, and a dict of responses level to IPV_Response objects.
    I recommend calling this in settings.py, with config, rules, and responses defined there."""
    global IPV_AUTH
    if not isinstance(IPV_AUTH, ipvAuthorizer):
        IPV_AUTH = ipvAuthorizer()
    if authview:
        IPV_AUTH.authview = authview()
    if config:
        IPV_AUTH.configure(config)
    if rules:
        IPV_AUTH.rules = rules
    if responses:
        IPV_AUTH.responses = responses
        

def validate(request):
    """Runs the IPV_AUTH's validator"""
    valid, request, context = IPV_AUTH.validate_request(request)
    if valid:
        #if it's valid, we'll return the ValidResponse
        return ValidResponse
    else:
        #We've got something to do here. Call the IPV_AUTH.authview's get.
        response = IPV_AUTH.authview.get(request, context)
        return response
    
    