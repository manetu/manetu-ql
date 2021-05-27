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
from string import Template

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

    data = cmds[args.subcmd](gql, args)

    if data != None:
        if args.pretty:
            print(json.dumps(json.loads(data), indent=2))
        else:
            print(data)
    elif args.verbose > 0:
        print("No data")
        sys.exit(1)


def vlist(gql, args):
    if verbosity > 0:
        print('executing "list" subcommand')

    scopes = ['ALL', 'CLAIMED', 'UNCLAIMED', 'REJECTED']
    scope = None
    for tt in args.terms:
        if tt in scopes:
            scope = tt
            break
    
    spec = 'scope:ALL'
    if scope != None:
        spec = f'scope:{scope}'
    elif len(args.terms) > 0:
        spec = f'labels:{json.dumps(args.terms)}'

    fields = get_vault_fields(gql, args.full, args.attributes, args.iri)

    query = f'{{ get_provider_vaults({spec}) {{ {" ".join(fields)} }}  }}'

    if verbosity > 1:
        print(f'using query text: {query}')

    data = gql.query(query)

    return data

def search(gql, args):
    pass

def create(gql, args):
    if verbosity > 0:
        print('executing "create" subcommand')
        if len(args.terms) > 1:
            print(f'extraneous arguments passed: {args.terms[1:]}')
        print(f'creating vault: {args.terms[0]}')

    template = Template('{ create_vault(label:"$label", role: USER) { label sid created role } }')

    if verbosity > 1:
        print(f'using mutation text: {template.substitute(label=args.terms[0])}')

    data = gql.mutation(template.substitute(label=args.terms[0]))

    return data

def delete(gql, args):
    if verbosity > 0:
        print('executing "delete" subcommand')
        if len(args.terms) > 1:
            print(f'extraneous arguments passed: {args.terms[1:]}')
        print(f'deleting vault: {args.terms[0]}')

    template = Template('{ delete_vault(label:"$label") }')

    if verbosity > 1:
        print(f'using mutation text: {template.substitute(label=args.terms[0])}')

    data = gql.mutation(template.substitute(label=args.terms[0]))

    return data


def lookup_object(gql, name):
    global schema
    if schema == {}:
        sch =''
        try:
            sch = get_schema(gql, 'all', True)
            schema = json.loads(sch)['data']['__schema']
        except:
            if verbosity > 2:
                print(f'Received data:\n {sch}')
            raise

    obj = None
    for v in schema['types']:
        if v['name'] == name:
            obj = v
            break
    return obj

def get_vault_fields(gql, full=False, attr=False, iri=False):
     # minimal field set
    if not full:
        return ['label', 'name']

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
            continue

        if field['type']['kind'] == 'OBJECT':
            obj = lookup_object(gql, field['type']['name'])
            if obj == None:
                continue
            flist.extend(get_obj_fields(gql, obj, field['name']))
            continue

        if field['type']['kind'] == 'LIST':
            # TODO:
            continue

    return flist

def get_obj_fields(gql, obj, fname):
    if fname != None:
        ret = [fname, '{']
    else:
        ret = [obj['name'], '{']

    for field in obj['fields']:
        if field['type']['kind'] == 'OBJECT':
            inobj = lookup_object(gql, field['type']['name'])
            if inobj == None:
                continue
            ret.extend(get_obj_fields(gql, inobj, field['name']))
            continue

        if field['type']['kind'] == 'ENUM' or field['type']['kind'] == 'SCALAR':
            ret.append(field['name'])
            continue

        if field['type']['kind'] == 'LIST':
            #TODO:
            continue

    ret.append('}')
    if verbosity > 1:
        print(f'got object: {ret}')
    return ret
