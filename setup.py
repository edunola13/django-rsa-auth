import os
from setuptools import setup, find_packages


path = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(path, 'README.md')).read()


setup(
    name='rsa_auth',
    version='0.1',
    packages=find_packages(),
    description='Django RSA Auth',
    long_description=README,
    author='eduardo',
    author_email='edunola13@gmail.com',
    package_data={
        '': ['*.txt', '*.html']
    },
    include_package_data=True,
    url='https://github.com/edunola13/django-rsa-auth/',
    license='MIT',
)
