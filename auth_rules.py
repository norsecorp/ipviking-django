#===============================================================================
# This module contains rules for IPViking to use in determining behavior. These
# checks will be executed in order, with the highest-numbered behavior being 
# executed. Because each rule is passed the full IPiking query, you can set 
# conditions based on multiple fields, as seen below.

# The first example filter defines different actions based on risk factor
# The second example filter uses pre-defined lists to respond to locations
# The third example shows fine filtering, blocking only botnets from the US
#===============================================================================

from ipviking_auth.forms import LoginForm, EmailForm
import sys, os
sys.path.append(os.getcwd()+'/ipviking-api-python')
from wrapper import IPViking


IPVIKING_CONFIG = {'proxy':'beta.ipviking.com','apikey':'8292777557e8eb8bc169c2af29e87ac07d0f1ac4857048044402dbee06ba5cea'}
 
IPV = IPViking(config = IPVIKING_CONFIG)

# This is the method to call from outside the module

def ipv_action(request, ip):
    success, data = IPV.request({'method':'ipq','ip':ip})
    if not success:
        return None

    checks = {0:[]}
    for level, check, warning in IPVIKING_CHECKS:
        flagged = check(data)
        if not flagged:
            continue
        else:
            if level in checks:
                checks[level].append(warning)
            else:
                checks[level] = [warning]
    
    response_level = max(checks.keys())
    warnings = checks[response_level]
    return IPVIKING_RESPONSES[response_level](request, response_level, warnings, data)
    

# These are response-context builders    

def block(request, level, ipviking_warnings):
    request.session['ipviking'] = level
    return {'state':"Your host address has been blocked, due to %s." % ','.join(ipviking_warnings),
            'template':'home.html',
            'request':request}

def require_login(request, level, ipviking_warnings):
    request.session['ipviking'] = level
    form = LoginForm()
    return {'state':"We'll need you to log in. Your host address has been flagged, due to %s." % ','.join(ipviking_warnings),\
            'form':form,
            'template':'auth.html',
            'request':request}

def require_email(request, level, ipviking_warnings, data):
    request.session['ipviking'] = level
    form = EmailForm()
    return {'state':"We'll need you to provide an email so that we can track your session \n. Your host address has been flagged, due to %s." % ','.join(ipviking_warnings),\
            'form':form,
            'template':'auth.html',
            'request':request} 

def allow_access(request, level, ipviking_warnings):
    request.session['ipviking'] = level
    return {'request', request}


# These are the rules for validating with IPViking data

BLOCKED_COUNTRIES = ['Madagascar']
WARN_COUNTRIES = ['United States']

IPVIKING_CHECKS = [
                (1,lambda data: data['risk_factor'] > 50, "suspicious behavior"),
                (2,lambda data: data['risk_factor'] > 70, "suspicious behavior"), 
                (3,lambda data: data['risk_factor'] > 90, "suspicious behavior"),

                (1,lambda data: data['geoloc']['country'] in WARN_COUNTRIES, "location"),
                (3,lambda data: data['geoloc']['country'] in BLOCKED_COUNTRIES, "location"),
                
                (3,lambda data: data['geoloc']['country'] in WARN_COUNTRIES and \
                        '5' in [entry['category_id'] for entry in data['entries']], "botnet-like behavior")]

IPVIKING_RESPONSES = {3:block,
                     2:require_login,
                     1:require_email,
                     0:allow_access
                        }
