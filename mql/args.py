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

# ----- global options -----
parser.add_argument('-v', '--verbose', action='count', default=0,
                    help='increase verbose output')
parser.add_argument('-p', '--pat', action='store',
                    help='specify personal access token to use')
parser.add_argument('-j', '--jwt', action='store',
                    help='specify jwt to use')

#  the commands container
subparsers = parser.add_subparsers(help='commands', dest='command')


#  ----- schema command ------
schema_parser = subparsers.add_parser('schema', help='get schema from server')


#  ----- getall command which gets all fields in an object ------
getall_parser = subparsers.add_parser('getall', help='get all fields for an object')
getall_parser.add_argument('object', action='store',
                           help='the object of interest')
