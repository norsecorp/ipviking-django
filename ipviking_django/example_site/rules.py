"""This module contains examples rules and responses for the ipvAuth class"""

#===============================================================================
# This module contains rules for IPViking to use in determining behavior. These
# checks will be executed in order, with the highest-numbered behavior being 
# executed. Because each rule is passed the full IPiking query, you can set 
# conditions based on multiple fields, as seen below.

# The first example filter defines different actions based on risk factor
# The second example filter uses pre-defined lists to respond to locations
#===============================================================================

from ipviking_django.forms import LoginForm, EmailForm
from ipviking_django.models import IPV_Rule, IPV_Response, ValidResponse
from ipviking_api_python.helpers.constants import SANDBOX_APIKEY, PROXIES

EXAMPLE_CONFIG = {'apikey':SANDBOX_APIKEY, 'proxy':PROXIES['SANDBOX']}

BLOCKED_COUNTRIES = ['Madagascar']
WARN_COUNTRIES = ['United States']

#these are the rules for authentication
risk_factor_low = IPV_Rule(check = lambda data: int(data) > 70, fields=['risk_factor'], warning = "suspicious net traffic", response = 1)
risk_factor_high = IPV_Rule(check = lambda data: int(data) > 90, fields=['risk_factor'], warning = "suspicious net traffic", response = 5)
geoloc_low = IPV_Rule(check = lambda data: data in WARN_COUNTRIES, fields=['geoloc','country'], warning = "location", response = 1)
geoloc_high = IPV_Rule(check = lambda data: data in BLOCKED_COUNTRIES, fields=['geoloc','country'], warning = "location", response = 5)

IPVIKING_RULES = [risk_factor_low, geoloc_low, risk_factor_high, geoloc_high]

# These are response-context builders
block = IPV_Response(state = "Your host address has been blocked, due to %s.", template = 'home.html', response_context = {})
require_login = IPV_Response(state = "We'll need you to log in. Your host address has been flagged due to %s.", template = 'auth.html', response_context = {'form', LoginForm()})
require_email = IPV_Response(state = "We'll need you to provide an email. Your host address has been flagged due to %s.", template = 'auth.html', response_context = {'form':EmailForm()})

IPVIKING_RESPONSES = {0:ValidResponse,
                      1:require_email,
                      5:block}