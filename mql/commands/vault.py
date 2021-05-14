"""List and manipulate vaults in the GraphQL server"""

__copyright__ = """
Copyright (C) 2021 Manetu Inc.
Author: Alex Tsariounov <alext@manetu.com>

This is free software; please see the LICENSE file
for details and any restrictions.
"""

from mql.args import vault_parser
from mql.commands.schema import get_schema
import json, sys

verbosity = 0
schema = {}

def dispatch(gql, args, remainder):
    """gql: an intialized GQL object, args: the parsed arguments"""
    global verbosity
    verbosity = args.verbose

    if args.subcmd == None:
        print('Error: vault subcommand not specified')
        vault_parser.print_usage()
        sys.exit(1)

    if verbosity > 1:
        print(f'executing "vault" command, verbosity {verbosity}')

    args.terms.extend(remainder)  # add potentially negated terms (for search)

    if verbosity > 1:
        print(f"args: {args}")

    cmds = {
        'list': vlist,
        'search': search,
        'create': create,
        'delete': delete
    }

    if args.subcmd not in cmds:
        raise ValueError(f'unknown command requested: "{args.subcmd}"')

    data = cmds[args.subcmd](gql, args.terms, args.full)

    if args.pretty:
        print(json.dumps(json.loads(data), indent=2))
    else:
        print(data)


def vlist(gql, terms, full):
    if verbosity > 0:
        print('executing "list" subcommand')

    scopes = ['ALL', 'CLAIMED', 'UNCLAIMED', 'REJECTED']
    scope = None
    for tt in terms:
        if tt in scopes:
            scope = tt
            break
    
    spec = 'scope:ALL'
    if scope != None:
        spec = f'scope:{scope}'
    elif len(terms) > 0:
        spec = f'labels:{terms}'

    fields = get_vault_fields(gql, full)

    query = f'{{ get_provider_vaults({spec}) {{ {" ".join(fields)} }}  }}'

    if verbosity > 1:
        print(f'using query text: {query}')

    data = gql.query(query, None)

    return data

def search(gql, terms, full):
    pass

def create(gql, terms, full):
    pass

def delete(gql, terms, full):
    pass


def lookup_object(gql, name):
    global schema
    if schema == {}:
        schema = json.loads(get_schema(gql, 'all', True))['data']['__schema']

    obj = None
    for v in schema['types']:
        if v['name'] == name:
            obj = v
            break
    return obj

def get_vault_fields(gql, full=False):
     # minimal field set
    if not full:
        return ['label']

    # full field set
    vault = lookup_object(gql, 'vault')
    if vault == None:
        raise ValueError("can't find 'vault' object in schema")

    flist = []
    for field in vault['fields']:
        # skip attributes for now
        if field['name'] == 'attributes':
            continue

        if field['type']['kind'] == 'ENUM' or field['type']['kind'] == 'SCALAR':
            flist.append(field['name'])
            continue

        if field['type']['kind'] == 'NON_NULL' and field['type']['ofType']['kind'] == 'SCALAR':
            flist.append(field['name'])

    return flist
