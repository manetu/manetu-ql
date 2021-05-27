#!/usr/bin/env python

from setuptools import setup
from mql.version import version

def readme():
    with open('README.md') as f:
        return f.read()

setup(name = 'manetu_ql',
    version = version, 
    license = 'MIT with minor restrictions',
    author = 'Alex Tsariounov',
    author_email = 'alext@manetu.com',
    url = 'http://github.com/manetu/manetu-ql',
    description = 'A sample python application that demonstrates GraphQL access to Manetu.io',
    long_description = readme(),
    scripts = ['manetu-ql'],
    packages = ['mql', 'mql.commands', 'mql.commands.graphql'],
    data_files = [
        ('share/doc/manetu-ql', ['README.md', 'LICENSE'])
        ],
    options = { 'sdist': { 'owner' : 'root', 'group' : 'root' } },
    zip_safe=False
    )
