"""Describe an object from the introspective GraphQL server"""

__copyright__ = """
Copyright (C) 2021 Manetu Inc.
Author: Alex Tsariounov <alext@manetu.com>

This is free software; please see the LICENSE file
for details and any restrictions.
"""

from mql.args import describe_parser
from mql.resolver import cmd_resolve
from mql.commands.schema import get_schema
import importlib, json, sys

verbosity = 0
schema = {}
mygql = None

def dispatch(gql, args, remainder):
    """gql: an intialized GQL object, args: the parsed arguments"""
    global mygql
    mygql = gql
    verbosity = args.verbose

    if verbosity > 1:
        print(f'executing "describe" command, verbosity {verbosity}')

    obj = lookup_object(args.object)

    if obj is None:
        raise ValueError(f'unknown object requested: "{args.object}"')

    if len(remainder) > 0:
        print(f'unknown extra arguments passed: {remainder}')
        describe_parser.print_usage()
        sys.exit(1)

    result = {
        'kind': obj['kind'],
        'name': obj['name'],
    }

    if obj['description'] != None:
        result['description'] = obj['description']

    if obj['kind'] == 'ENUM':
        result['enumValues'] = extract_enumValues(obj)

    if 'inputFields' in obj and obj['inputFields'] != None and len(obj['inputFields']) > 0:
        fields = extract_fields(obj, 'inputFields', input=True)
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


def extract_fields(obj, section, input=False):
    """extract and create dict of fields from specified json object in specified section (fields, inputFields, args)"""
    fields = []

    if input:
        f_type = 'type'
        f_kind = 'kind'
    else:
        f_type = 'returns_type'
        f_kind = 'returns_kind'

    for v in obj[section]:
        r = {}
        r['name'] = v['name']
        if 'type' in v:
            r[f_kind] = v['type']['kind']

        if f_kind in r and r[f_kind] == 'ENUM':
            enum = lookup_object(v['type']['name'])
            r['enumValues'] = extract_enumValues(enum)
            
        if v['type']['ofType'] == None:
            r[f_type] = v['type']['name']
        else:
            r[f_type], r['ofType'] = extract_ofType(v)
            if r['ofType'].endswith("ENUM"):
                enum = lookup_object(r[f_type])
                r['enumValues'] = extract_enumValues(enum)

        if v['description'] != None:
            r['description'] = v['description']
        if 'defaultValue' in v and v['defaultValue'] != None:
            r['defaultValue'] = v['defaultValue']

        if 'args' in v and v['args'] != None and len(v['args']) > 0:
            args = extract_fields(v, 'args', input=True)
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
