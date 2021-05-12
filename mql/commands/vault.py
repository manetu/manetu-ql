"""List and manipulate vaults in the GraphQL server"""

__copyright__ = """
Copyright (C) 2021 Manetu Inc.
Author: Alex Tsariounov <alext@manetu.com>

This is free software; please see the LICENSE file
for details and any restrictions.
"""

from mql.args import vault_parser
from mql.commands.schema import get_schema
import sys

verbosity = 0
schema = {}
mygql = None

def dispatch(gql, args, remainder):
    """gql: an intialized GQL object, args: the parsed arguments"""
    global mygql
    mygql = gql
    verbosity = args.verbose

    if args.subcmd == None:
        print('Error: vault subcommand not specified')
        vault_parser.print_usage()
        sys.exit(1)

    if verbosity > 1:
        print(f'executing "list" command, verbosity {verbosity}')

    args.terms.extend(remainder)  # add potentially negated terms

    print(f"Args: {args}")
