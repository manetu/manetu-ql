"""Main module for example code to access the Manetu.io GraphQL interface."""

__copyright__ = """
Copyright (C) 2021 Manetu Inc.
Author: Alex Tsariounov <alext@manetu.com>

This is free software; please see the LICENSE file
for details and any restrictions.
"""

from mql.version import version
from mql.args import parser
import argparse, importlib, sys


# cmdline entry point and dispatcher
def main():
    args = parser.parse_args()

    if args.verbose:
        print(f'Manetu.io GraphQL interface, version {version}')
        if args.verbose > 1:
            print(f'dispatching command: "{args.command}", with verbosity of {args.verbose}')

    try:
        if args.command == None:
            print('Error: command not specified')
            parser.print_usage()
            sys.exit(1)

        # first import the command
        cmd = importlib.import_module(f'mql.commands.{args.command}')

        # check for the pat
        if args.pat == None and args.jwt == None:
            print('no PAT or JWT specified, cannot login to manetu.io')
            # TODO: here is where we'll impl oauth logins
            sys.exit(1)

        # and now execute it
        cmd.dispatch(args)

    except SystemExit:
        raise

    except:
        print(f'Unexpected error for command: {args.command}, error: {sys.exc_info()[1]}')
        sys.exit(2)
