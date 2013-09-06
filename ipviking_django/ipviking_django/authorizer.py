"""This module contains the ipvAuth instance to handle authentications"""
import ipviking_api_python.helpers.constants as ipv_consts
from ipviking_api_python.auth.objects import ipvAuthorizer

APIKEY = ipv_consts.SANDBOX_APIKEY
PROXY = ipv_consts.PROXIES['SANDBOX']    
IPV_AUTH = ipvAuthorizer().configure(apikey = APIKEY, proxy = PROXY)

def configure(rules = None, responses = None, apikey = None, proxy = None, authview = None, validview = None):
    try:
        IPV_AUTH.configure(apikey = apikey, proxy = proxy, rules = rules, responses = responses, authview = authview(), validview = validview)
    except:
        global IPV_AUTH
        IPV_AUTH = ipvAuthorizer()
        IPV_AUTH.configure(apikey = apikey, proxy = proxy, rules = rules, responses = responses, authview = authview(), validview = validview)

def validate(request):
    """Runs the IPV_AUTH's validator"""
    orig_path = request.path
    if request.session.get('ipviking'):
        return None
    else:
        ip = request.get_host().split(':')[0]
        if ip == '127.0.0.1':
            ip = '208.74.76.5'
        valid, request, level, context = IPV_AUTH.validate_request(request, ip)
        if valid:
            #if it's valid, we'll return the validview (redirect to request.path)
            request.session['ipviking'] = level
            return IPV_AUTH.validview(request, orig_path)
        else:
            #We've got something to do here. Call the IPV_AUTH.authview's get.
            response = IPV_AUTH.authview.get(request, context)
            return response
        
