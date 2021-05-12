"""Get the schema from the introspective GraphQL server."""

__copyright__ = """
Copyright (C) 2021 Manetu Inc.
Author: Alex Tsariounov <alext@manetu.com>

This is free software; please see the LICENSE file
for details and any restrictions.
"""

from mql.resolver import cmd_resolve
from mql.args import schema_cmds, schema_parser
import importlib, json, sys

verbosity = 0


def dispatch(gql, args, remainder):
    """gql: an intialized GQL object, args: the parsed arguments"""
    verbosity = args.verbose

    if verbosity > 1:
        print(f'executing "schema" command, verbosity {verbosity}')

    desired = cmd_resolve(args.desired, schema_cmds)
    
    if len(remainder) > 0:
        print(f'unknown extra arguments passed: {remainder}')
        schema_parser.print_usage()
        sys.exit(1)
    
    data = get_schema(gql, desired, args.full)

    if args.pretty:
        print(json.dumps(json.loads(data), indent=2))
    else:
        print(data)


def get_schema(gql, desired, full=False):
    """gql: an initialized GQL object, desired: all/queries/mutations/subscriptions, full: all or terse"""
    mod = importlib.import_module(f'mql.commands.graphql.schema-{desired}')

    if full:
        query = mod.queryFull
    else:
        query = mod.queryShort

    if verbosity > 1:
        print(f'using query text: {query}')

    # let it raise on errors
    data = gql.query(query, None)

    # output pretified json
    if verbosity > 0:
        print('Server returns:')

    return data
