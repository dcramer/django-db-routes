#!/usr/bin/env python
import sys
from os.path import dirname, abspath

sys.path.insert(0, dirname(abspath(__file__)))

from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES={
            # XXX: due to bugs in Django, we must have a default connection
            # so it can generate db_table names (including for abstract models)
            'default': {
                'ENGINE': 'dbroutes.backend',
                'NAME': 'dbroutes',
                'HOST': 'localhost',
            },
            'cluster': {
                'NAME': 'dbroutes',
                'SHARDS': 1024,
                'HOSTS': [
                    {'HOST': 'localhost'},
                ],
            },
        },
        INSTALLED_APPS=[
            'tests',
        ],
        ROOT_URLCONF='',
        DEBUG=False,
    )

import dbroutes
dbroutes.install(settings=settings)
