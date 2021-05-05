"""Describe an object from the introspective GraphQL server"""

__copyright__ = """
Copyright (C) 2021 Manetu Inc.
Author: Alex Tsariounov <alext@manetu.com>

This is free software; please see the LICENSE file
for details and any restrictions.
"""

from mql.resolver import cmd_resolve
from mql.args import describe_cmds
from mql.commands.schema import get_schema
import importlib, json

verbosity = 0

def dispatch(gql, args):
    """gql: an intialized GQL object, args: the parsed arguments"""
    verbosity = args.verbose

    if verbosity > 1:
        print(f'executing "schema" command, verbosity {verbosity}')

    how = cmd_resolve(args.how, describe_cmds)

    schema = json.loads(get_schema(gql, 'all', True))['data']['__schema']

    obj = None
    for v in schema['types']:
        if v['name'] == args.object:
            obj = v
    
    if obj is None:
        raise ValueError(f'unknown object requested: "{args.object}"')

    result = {
        'kind': obj['kind'],
        'name': obj['name'],
    }
    if obj['description'] != None:
        result['description'] = obj['description']

    if obj['kind'] == 'ENUM':
        vals = []
        for ev in obj['enumValues']:
            vals.append(ev['name'])
        if len(vals) > 0:
            result['enumValues'] = vals

    if how != 'short':
        if how == 'returns' or how == 'all':
            if 'type' in obj:
                # this is a return object
                pass
        if how == 'args' or how == 'all':
            if 'args' in obj and obj['args'] != None and len(obj['args']) > 0:
                pass
        if how == 'fields' or how == 'all':
            if 'inputFields' in obj and obj['inputFields'] != None and len(obj['inputFields']) > 0:
                fields = []
                for v in obj['inputFields']:
                    r = {}
                    r['name'] = v['name']
                    r['kind'] = v['type']['kind']
                    if v['type']['name'] != None:
                        r['type'] = v['type']['name']
                    else:
                        r['ofType'] = v['type']['ofType']['kind']
                        r['type'] = v['type']['ofType']['name']
                    if v['description'] != None:
                        r['description']
                    if v['defaultValue'] != None:
                        r['defaultValue'] = v['defaultValue']
                    fields.append(r)
                if len(fields) > 0:
                    result['inputFields'] = fields
            if 'fields' in obj and obj['fields'] != None and len(obj['fields']) > 0:
                fields = []
                for v in obj['fields']:
                    r = {}
                    r['name'] = v['name']
                    r['kind'] = v['type']['kind']
                    if v['type']['name'] != None:
                        r['type'] = v['type']['name']
                    else:
                        r['ofType'] = v['type']['ofType']['kind']
                        r['type'] = v['type']['ofType']['name']
                    if v['description'] != None:
                        r['description'] = v['description']
                    if 'defaultValue' in v and v['defaultValue'] != None:
                        r['defaultValue'] = v['defaultValue']
                    fields.append(r)
                if len(fields) > 0:
                    result['fields'] = fields

    if args.pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))
