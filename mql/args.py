"""Arguments parsing scaffold"""

__copyright__ = """
Copyright (C) 2021 Manetu Inc.
Author: Alex Tsariounov <alext@manetu.com>

This is free software; please see the LICENSE file
for details and any restrictions.
"""

from mql.version import version
import argparse

# parser declarations for common and all subcommands
parser = argparse.ArgumentParser(description=f'Manetu.io GraphQL interface, version {version}')

# ----- defaults -----
defURI = 'https://portal.eu.manetu.io/graphql'
defPAT = 'MANETUQL_PAT'
defJWT = 'MANETUQL_JWT'

# ----- global options -----
parser.add_argument('-v', '--verbose', action='count', default=0,
                    help='increase verbose output')
parser.add_argument('-u', '--uri', action='store',
                    help=f'the URI of the GraphQl server (default: "{defURI}")',
                    default=defURI)
parser.add_argument('-p', '--pat', action='store',
                    help='specify env var that holds the personal access token (default: "MANETUQL_PAT")')
parser.add_argument('-j', '--jwt', action='store',
                    help='specify env var that holds the jwt (default: "MANETUQL_JWT")')
parser.add_argument('--pretty', action='store_true',
                    help="pretty-print json output, or pipe to 'jq' (default: compact output)")


#  the commands container
subparsers = parser.add_subparsers(help='commands', dest='command')


#  ----- schema command ------
schema_cmds = ['all', 'queries', 'mutations', 'subscriptions']
schema_parser = subparsers.add_parser('schema', help='get schema from server')
schema_parser.add_argument('desired', action='store',
                            help=f"which schema to get (default: 'all', choices: {schema_cmds})",
                            nargs='?', default='all')
schema_parser.add_argument('-f', '--full', action='store_true',
                            help='output full schema (default: list of name/description)')

#  ----- list command which lists all objects so you can describe/user them -----
list_parser = subparsers.add_parser('list', help='list all objects so you can describe/use them')

#  ----- getall command which gets all fields in an object ------
# getall_parser = subparsers.add_parser('getall', help='get all fields for an object')
# getall_parser.add_argument('object', action='store',
#                            help='the object of interest')

#  ----- describe command which descirbes objects so you can call/specify them -----
describe_parser = subparsers.add_parser('describe', help='describe an object so you can call/use it')
describe_parser.add_argument('object', action='store',
                             help='which object to describe')

#  ----- vault command which is used to create/destory/update vaults and list them -----
vault_parser = subparsers.add_parser('vault', help='manage vaults in system')

vsubparsers = vault_parser.add_subparsers(help='subcommands', dest='subcmd')

vlist_parser = vsubparsers.add_parser('list', help='list vaults in system')
vlist_parser.add_argument('terms', action='store',
                          help='which vault(s) to list (a list of vault labels), or which scopes (ALL, CLAIMED, UNCLAIMED, REJECTED), blank lists ALL',
                          nargs='*', default=['ALL'])
vlist_parser.add_argument('-f', '--full', action='store_true',
                            help='output all vault fields (default: minimal)')
vlist_parser.add_argument('-a', '--attributes', action='store_true',
                            help='include attributes in output')
vlist_parser.add_argument('-i', '--iri', action='store_true',
                            help="include iri's in output")

vsearch_parser = vsubparsers.add_parser('search', help='search for vaults matching term(s)')
vsearch_parser.add_argument('terms', action='append',
                            help='search terms, implied "and", possibly containing negated terms (ie "match_this -but_not_this")',
                            nargs='?')
vsearch_parser.add_argument('-f', '--full', action='store_true',
                            help='output all vault fields (default: minimal)')
vsearch_parser.add_argument('-a', '--attributes', action='store_true',
                            help='include attributes in output')
vsearch_parser.add_argument('-i', '--iri', action='store_true',
                            help="include iri's in output")

vcreate_parser = vsubparsers.add_parser('create', help='create vault(s)')
vcreate_parser.add_argument('terms', action='store',
                            help='create a vault with given label, multiple labels will create multiple vaults',
                            nargs='+')

vdelete_parser = vsubparsers.add_parser('delete', help='delete vault(s)')
vdelete_parser.add_argument('terms', action='store',
                            help='delete a vault with given label, multiple labels will delete multiple vaults',
                            nargs='+')
