"""List and manipulate vaults in the GraphQL server"""

__copyright__ = """
Copyright (C) 2021 Manetu Inc.
Author: Alex Tsariounov <alext@manetu.com>

This is free software; please see the LICENSE file
for details and any restrictions.
"""

from mql.resolver import cmd_resolve
from mql.commands.schema import get_schema
import importlib, json

verbosity = 0
schema = {}
mygql = None

def dispatch(gql, args):
    """gql: an intialized GQL object, args: the parsed arguments"""
    global mygql
    mygql = gql
    verbosity = args.verbose

    if verbosity > 1:
        print(f'executing "list" command, verbosity {verbosity}')

    print(f"Args: {args}")
