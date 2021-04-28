"""Get the schema from the introspective GraphQL server."""

__copyright__ = """
Copyright (C) 2021 Manetu Inc.
Author: Alex Tsariounov <alext@manetu.com>

This is free software; please see the LICENSE file
for details and any restrictions.
"""

from mql.gql import GQL
import importlib, json

def dispatch(args):
    if args.verbose > 1:
        print(f'executing "schema" command, verbosity {args.verbose}')

    mod = importlib.import_module(f'mql.commands.graphql.schema-{args.desired}')

    if args.full:
        query = mod.queryFull
    else:
        query = mod.queryShort

    if args.verbose > 1:
        print(f'using query text: {query}')

    gq = GQL({'Authorization': args.tokStr}, args.uri, args.verbose)

    # let it raise on errors
    data = gq.query(query, None)

    # output pretified json
    if args.verbose > 0:
        print('Server returns:')
    
    print(data)
