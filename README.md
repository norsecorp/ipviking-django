DEMO: IPVIKING IN CLIENT AUTHENTICATION

Implementing the IPViking Python API is simple. You'll need two things: the ipviking_auth plugin for Django (let's assume
that you have that, since you're reading this), and the API itself, which can be found at http://github.com/norsecorp/ipviking-api-python
Then follow the below instructions for a guide on installation.

QUICK-AND-EASY-VERSION:
1) Download the ipviking_auth and ipviking-api-python packages.
2) Replace the path in line 14 of ipviking_auth.auth_rules with the path to your ipviking-api-python package.
3) Replace DEFAULTCONFIG in ipviking_auth.auth_rules with {'apikey':<your API key>, 'proxy':<the appropriate proxy>}
3) Choose the authentication rules you'd like to follow by modifying the IPVIKING_CHECKS variable (see below for help)
4) Any view that you want protected, just have it inherit from ipviking_auth.views.BaseView


THE IN-DEPTH VERSION:	

THE IPVIKING-API-PYTHON PACKAGE:
This package handles the backend- building a request to our server and parsing the response. It returns a dictionary if there's valid 
data, and a string if an error is raised. For a Django application, you shouldn't need to do much with this, but feel free to poke around!

THE IPVIKING-AUTH PACKAGE
This is the package you'll actually have to handle. First things first, do steps 2 and 3 from the quick and easy version. Your API key can be
found under account details on https://ipviking.com/, and the proxies can be found under developers.

We'll touch on custom authentication rules in a bit- first let's go over implementation. For convenience, the ipviking authentication is
built into a custom BaseView class in views. This overwrites the View.as_view() and adds the authentication check. To use it, simply have
your views inherit from BaseView. If you prefer method-based views, you can copy the code from lines 32-39 into the method and it should run.

The ipv_auth module is where the work happens- this contains the call to ipviking-api-python and your responses to threat data. The general 
structure of the module is as follows:

-IPVIKING_CHECKS: these are checks to be performed on the data called from the IPViking request- in short, your rules for determining 
	who poses a danger. It's a list of 2-tuples; the first value of each tuple is the response type, the second is the boolean check.
	As it's currently set up, the highest response code wins, so construct your checks and responses in a way such that a higher code 
	merits a stricter response.

-IPVIKING_RESPONSES: this is a simple map of response code to methods.

-block, allow_access, require_login, etc- these are methods to build a response context, plus the former request and a template. They 
	map to the response codes.
	
-ipv_action: This is the method to call from outside the module- pass it an IP address, it'll perform the check and return an appropriate
	context. From there, you can simple pop out the template and use render_to_response- as you'll see in auth.views.AuthView
	
Finally, we have views.AuthView. This is simply a view that's called from the BaseView check, and it renders the data from the ipv_action
method. It also sets the 'ipviking' value in the request.session field, so you're not stuck performing this check every time. It references
forms set in forms.py, but that's pretty much straight out of the Django documentation.


That should be about all! Happy developing!