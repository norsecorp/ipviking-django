"""Here's our handy setup script for the ipviking django authentication"""

from setuptools import setup

setup(
      name = 'ipviking_django',
      version = '0.1',
      description = 'An easy-to-use wrapper for using IPViking to assist authentication in a Django app.',
      author = 'Marcus Hoffman',
      url = 'https://github.com/norsecorp/ipviking-django',
      license = 'BSD',
      packages = ['ipviking_django', 'ipviking_django.example_site'],
      include_package_data = True,
      package_data = {'':['README.md']},
      install_requires = ['ipviking_api_python'],
      tests_require = [],
      classifiers = ['Development Status :: 1 - Beta',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: BSD Licence',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     'Topic :: Internet',
                     'Topic :: Network Security',
                     'Topic :: Software Development :: Libraries :: Python Modules'])