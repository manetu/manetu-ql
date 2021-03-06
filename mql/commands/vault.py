"""List and manipulate vaults in the GraphQL server"""

__copyright__ = """
Copyright (C) 2021 Manetu Inc.
Author: Alex Tsariounov <alext@manetu.com>

This is free software; please see the LICENSE file
for details and any restrictions.
"""

from mql.args import vault_parser
from mql.commands.schema import get_schema
import copy, json, sys
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

    if args.terms == None:
        args.terms = remainder
    else:
        if len(args.terms) == 1 and args.terms[0] == None:
            args.terms = remainder
        else:
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

    if args.verbose > 0 and data == None:
        print("No data")
        sys.exit(1)

    # post process attributes if requested
    jdo = json.loads(data)
    for section in jdo['data']:                   # for subcommands in result
        jres = {'data': {section: ''}}
        jres['data'][section] = []
        for vault in jdo['data'][section]:            # for vaults in subcommand
            v = {}
            for attrkey in vault:                      # for items in vault
                if attrkey != 'attributes':
                    v[attrkey] = copy.deepcopy(vault[attrkey])
                    continue
                
                if not args.attributes:
                    continue

                v['attributes'] = []                   # process attributes
                for attrgroup in vault[attrkey]:
                    attr = {}
                    for attritem in attrgroup:         # for every triple
                        if attritem['name'] == '?p':        # name
                            name = attritem['value']
                        elif attritem['name'] == '?o':      # value
                            value = attritem['value']
                        elif attritem['name'] == '?s':      # iri
                            iri = attritem['value']
                        else:
                            raise ValueError(f'''unknown marker in attribute "{attritem["name"]}" : "{attritem["value"]}"''')
                    if args.prefix:
                        attr['name'] = name.strip('<>')
                    else:
                        sname = name.strip('<>').split(sep='#', maxsplit=1)
                        if len(sname) == 1:
                            attr['name'] = sname[0]
                        else:
                            attr['name'] = sname[1]
                    if args.iri:
                        attr['iri'] = iri.strip('<>')
                    attr['value'] = value.strip('<>')
                    v['attributes'].append(attr)

            jres['data'][section].append(v)

    if args.pretty:
        print(json.dumps(jres, indent=2))
    else:
        print(json.dumps(jres))


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

    fields = get_vault_fields(gql, args.full, args.attributes)
    if verbosity > 2:
        print(f'fields are: {fields}')
    query = f'{{ get_provider_vaults({spec}) {{ {" ".join(fields)} }}  }}'

    if verbosity > 1:
        print(f'using query text: {query}')

    data = gql.query(query)

    return data

def search(gql, args):
    if verbosity > 0:
        print('executing "search" subcommand')
        print(f'search term{"s" if len(args.terms)>1 else ""}: {args.terms}')

    if len(args.terms) == 0:
        raise ValueError('no search terms')

    fields = get_vault_fields(gql, args.full, args.attributes)
    if verbosity > 2:
        print(f'fields are: {fields}')
    query = f'{{ search(term:"{" ".join(args.terms)}") {{ {" ".join(fields)} }} }}'

    if verbosity > 1:
        print(f'using query text: {query}')

    data = gql.query(query)

    return data

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

def get_vault_fields(gql, full=False, attr=False):
    flist = []

    if attr:
        # get full set of attrs, will post-process later
        flist.append('attributes(sparql_expr:"SELECT ?s ?p ?o WHERE { ?s ?p ?o }") { name value }')

    # minimal field set
    if not full:
        flist.extend(['label', 'name'])
        if verbosity > 2:
            print(f'flist: {flist}')
        return flist

    # full field set
    vault = lookup_object(gql, 'vault')
    if vault == None:
        raise ValueError("can't find 'vault' object in schema")

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

        if field['type']['kind'] == 'OBJECT' or field['type']['kind'] == 'LIST':
            obj = lookup_object(gql, field['type']['name'])
            if obj == None:
                continue
            flist.extend(get_obj_fields(gql, obj, field['name']))
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

        if field['type']['kind'] == 'NON_NULL' and field['type']['ofType']['kind'] == 'SCALAR':
            ret.append(field['name'])
            continue

        if field['type']['kind'] == 'LIST':
            tname, tkind = extractName_ofType(field)
            if tname == None:
                continue
            if tkind == 'SCALAR':
                ret.append(field['name'])
            else:
                inobj = lookup_object(gql, tname)
                if inobj != None:
                    ret.extend(get_obj_fields(gql, inobj, field['name']))
            continue

    ret.append('}')
    if verbosity > 1:
        print(f'got object: {ret}')
    return ret

def extractName_ofType(obj):
    name = obj['type']['name']
    kind = obj['type']['kind']
    ofType = obj['type']['ofType']
    while ofType != None:
        name = ofType['name']
        kind = ofType['kind']
        ofType = ofType['ofType']
    return name, kind
