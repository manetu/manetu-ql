"""List objects from GraphQL server"""

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
    global mygql, schema
    mygql = gql
    verbosity = args.verbose

    if verbosity > 1:
        print(f'executing "list" command, verbosity {verbosity}')

    schema = json.loads(get_schema(mygql, 'all', True))['data']['__schema']
   
    objlist = []
    for v in schema['types']:
        objlist.append({"name": v['name'], "kind": v['kind']})
        
    if args.pretty:
        print(json.dumps(objlist, indent=2))
    else:
        print(json.dumps(objlist))

    if verbosity > 0:
        print(f'Total object gathered: {len(objlist)}')
