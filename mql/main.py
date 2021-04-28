"""Main module for example code to access the Manetu.io GraphQL interface."""

__copyright__ = """
Copyright (C) 2021 Manetu Inc.
Author: Alex Tsariounov <alext@manetu.com>

This is free software; please see the LICENSE file
for details and any restrictions.
"""

from mql.version import version
import mql.args
import argparse, base64, importlib, os, sys


# cmdline entry point and dispatcher
def main():
    args = mql.args.parser.parse_args()

    if args.verbose:
        print(f'Manetu.io GraphQL interface, version {version}')
        if args.verbose > 1:
            print(f'dispatching command: "{args.command}", with verbosity of {args.verbose}')

    try:
        if args.command == None:
            print('Error: command not specified')
            mql.args.parser.print_usage()
            sys.exit(1)

        # first import the command
        cmd = importlib.import_module(f'mql.commands.{args.command}')

        if args.verbose > 1:
            print(f'arguments: {args}')

        tokStr = resolveTok(args)
        if tokStr == None:
            print('no PAT or JWT specified, cannot login to manetu.io')
            mql.args.parser.print_usage()
            sys.exit(1)

        args.tokStr = tokStr
        if args.verbose > 1:
            print(f'using token string: "{args.tokStr}"')
        
        # and now execute it
        cmd.dispatch(args)

    except SystemExit:
        raise

    except:
        if args.verbose > 1:
            raise
        print(f'Unexpected error for command: {args.command}, error: {sys.exc_info()[1]}')
        sys.exit(2)


def resolveTok(args):
    # check for the pat, which is perferred over jwt
    if args.pat == None:
        if args.jwt == None:
            # default env for PAT, if not present try JWT
            tok = os.environ.get(mql.args.defPAT)
            if tok == None or tok == '':
                # PAT not specified, try defualt JWT
                tok = os.environ.get(mql.args.defJWT)
                if tok == None or tok == '':
                    return None
                else:
                    return 'Bearer ' + tok
            else:
                return 'Basic ' + base64.b64encode(f':{tok}'.encode('utf-8'))
        else:
            # jwt env specified
            tok = os.environ.get(args.jwt)
            if tok == None or tok == '':
                return None
            else:
                return 'Bearer ' + tok
    else:
        # pat env specified
        tok = os.environ.get(args.pat)
        if tok == None or tok == '':
            return None
        return 'Basic ' + base64.b64encode(f':{tok}'.encode('utf-8'))
