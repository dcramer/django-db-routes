#!/usr/bin/env python

from setuptools import setup, find_packages


tests_require = [
    'flake8',
    'mock==0.8',
    'pytest',
    'pytest-django-lite',
]

install_requires = [
    'Django>=1.5,<1.6',
    'psycopg2',
]

setup(
    name='django-db-routes',
    version='0.1.0',
    author='David Cramer',
    author_email='dcramer@gmail.com',
    url='http://github.com/getsentry/django-db-routes',
    description='Shard management for the Django ORM',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    zip_safe=False,
    extras_require={
        'tests': install_requires + tests_require,
    },
    install_requires=install_requires,
    tests_require=tests_require,
    include_package_data=True,
    license='Apache License 2.0',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
