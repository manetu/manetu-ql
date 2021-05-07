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


#  ----- getall command which gets all fields in an object ------
getall_parser = subparsers.add_parser('getall', help='get all fields for an object')
getall_parser.add_argument('object', action='store',
                           help='the object of interest')

#  ----- describe command which descirbes objects so you can call/specify them -----
describe_parser = subparsers.add_parser('describe', help='describe an object so you can call/use it')
describe_parser.add_argument('object', action='store',
                             help='which object to describe')
