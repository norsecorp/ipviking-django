DEMO: IPVIKING AUTHENTICATION IN DJANGO APPS

This is a sample authentication backend using IPVIKING threat awareness to provide realistic, configurable responses
to clients based on detailed intelligence on their online activities. Installation is lightweight and easy, but if
you have a need for more advanced configurations, this readme will give a rundown on the different pieces of the package.

This package is dependent on the ipviking_api_python package, also available on NorseCorp's github.

QUICK INSTALL:
1) Install the ipviking_api_python package using setup.py
2) Install the ipviking_django package using setup.py
3) Create your rules and responses (look at ipviking_django.rules for some examples).
4) Configure the authenticator in your settings.py module using ipviking_django.authorizer.configure
	(again, there's an example in ipviking_django.settings)
5) To protect a view with IPViking, just have it inherit from ipviking_django.views.BaseView

That's all, folks!


SOURCE DIVE:
This is an in-depth look at the source of this package, for developers with more specialized needs (and the confidence to
hack the package around a bit). This package is pretty simple, but dependent on Django, so I'd recommend some familiarity 
with the Django framework before you muck around with things.
		

VIEWS.PY
Contains the BaseView that IPViking-protected pages will inherit and the AuthView which handles authentication. The important ones
are below; everything else is pretty simple.
	
	-BaseView: This is simply an overwrite of the as_view method which checks the session to see if the ipviking flag has been set,
		and calls for authentication if not.
		
	-AuthView: This is a sample authentication view.
		-get: renders the response template in the response context generated by the ipvAuthorizer with with appropriate context.
		-post: validates the form results, if a form was generated. Note: this method MUST set the 'ipviking' flag for the session!
			(otherwise, you'd be running validation every time any user wants to see a protected view. Bottleneck much?)
	
FORMS.PY
Contains the forms for the example authview and IPV_Responses. You'll probably use your own if you're using a custom AuthView. It's
pretty much textbook Django forms.

AUTHORIZER.PY:
This is the module where our master ipvAuthorizer lives. configure and validate are wrapper functions called from this module so that
we can keep that one master copy of the ipvAuthorizer.

	-IPV_AUTH is set up as a default version of the authorizer. Example rules, example responses, sandbox API key and proxy, sample
		authview. Hence configure, so that you can, well, configure it.

	-configure: Helper function to take any authview, rules, responses, config arguments and apply them to IPV_AUTH.
	
	-validate: Helper function to wrap the API call, IPV_AUTH's validation, and IPV_AUTH's authview. Pass it a request, it'll return
		the response your rules and authview dictate. This level of abstraction is intentional, so that this single function can be
		slotted into the BaseView with next to no mess.
		

Everything else in the installation is pretty much standard Django, fresh from django-admin. So you can see, it's pretty simple to get
set up!
