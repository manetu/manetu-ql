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
schema = {}
mygql = None

def dispatch(gql, args):
    """gql: an intialized GQL object, args: the parsed arguments"""
    global mygql
    mygql = gql
    verbosity = args.verbose

    if verbosity > 1:
        print(f'executing "schema" command, verbosity {verbosity}')

    obj = lookup_object(args.object)

    if obj is None:
        raise ValueError(f'unknown object requested: "{args.object}"')

    result = {
        'kind': obj['kind'],
        'name': obj['name'],
    }

    if obj['description'] != None:
        result['description'] = obj['description']

    if obj['kind'] == 'ENUM':
        result['enumValues'] = extract_enumValues(obj)

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
        if r['kind'] == 'ENUM':
            enum = lookup_object(v['type']['name'])
            r['enumValues'] = extract_enumValues(enum)
            
        if v['type']['ofType'] == None:
            r['type'] = v['type']['name']
        else:
            r['type'], r['ofType'] = extract_ofType(v)
            if r['ofType'].endswith("ENUM"):
                enum = lookup_object(r['type'])
                r['enumValues'] = extract_enumValues(enum)

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

def extract_ofType(obj):
    """extract string of ofType's"""
    name = obj['type']['name']
    kind = obj['type']['kind']
    obj_dive = obj['type']['ofType']

    while obj_dive != None:
        kind += f"|{obj_dive['kind']}"
        if obj_dive['ofType'] == None:
            name = obj_dive['name']
        obj_dive = obj_dive['ofType']

    return name, kind

def extract_enumValues(obj):
    vals = []
    for ev in obj['enumValues']:
        vals.append(ev['name'])
    return vals

def lookup_object(name):
    global schema
    if schema == {}:
        schema = json.loads(get_schema(mygql, 'all', True))['data']['__schema']
    obj = None
    for v in schema['types']:
        if v['name'] == name:
            obj = v
            break
    return obj
