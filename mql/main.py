"""Main module for example code to access the Manetu.io GraphQL interface."""

__copyright__ = """
Copyright (C) 2021 Manetu Inc.
Author: Alex Tsariounov <alext@manetu.com>

This is free software; please see the LICENSE file
for details and any restrictions.
"""

from mql.version import version
import argparse, importlib, sys

# global parser declarations
parser = argparse.ArgumentParser(description=f'Manetu.io GraphQL interface, version {version}')

parser.add_argument('command', action='store',
                    help='run the specified commmand (schema, getall)')

parser.add_argument('-v', '--verbose', action='count',
                    default=0,
                    help='increase verbose output')
parser.add_argument('-p', '--pat', action='store',
                    help='specify personal access token to use')

# cmdline entry point and dispatcher
def main():
    args = parser.parse_args()

    if args.verbose > 0:
        print(f'dispatching command: "{args.command}", with verbosity of {args.verbose}')

   

    try:
        # first import the command
        cmd = importlib.import_module(f'mql.commands.{args.command}')

        # check for the pat
        if args.pat == None:
            print('no personal access token specified, cannot login to manetu.io')
            # TODO: here is where we'll impl oauth logins
            sys.exit(1)

        # and now execute it
        cmd.doit(args)

    except SystemExit:
        raise

    except:
        print(f'Unexpected error for command: {args.command}, error: {sys.exc_info()[1]}')
        sys.exit(2)
