"""Describe an object from the introspective GraphQL server"""

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

def dispatch(gql, args):
    """gql: an intialized GQL object, args: the parsed arguments"""
    verbosity = args.verbose

    if verbosity > 1:
        print(f'executing "schema" command, verbosity {verbosity}')

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

    if 'type' in obj:
        # this is a return object
        pass

    if 'inputFields' in obj and obj['inputFields'] != None and len(obj['inputFields']) > 0:
        fields = extract_fields(obj, 'inputFields')
        if fields != None:
            result['inputFields'] = fields

    if 'fields' in obj and obj['fields'] != None and len(obj['fields']) > 0:
        fields = extract_fields(obj, 'fields')
        if fields != None:
            result['fields'] = fields

    if args.pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))


def extract_fields(obj, section):
    """extract and create dict of fields from specified json object in specified section (fields, inputFields, args)"""
    fields = []

    for v in obj[section]:
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
        if 'args' in v and v['args'] != None and len(v['args']) > 0:
            args = extract_fields(v, 'args')
            if args != None:
                r['args'] = args
        fields.append(r)

    if len(fields) > 0:
        return fields

    return None
