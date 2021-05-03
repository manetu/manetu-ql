"""Manetu.io command resolver"""

__copyright__ = """
Copyright (C) 2021 Manetu Inc.
Author: Alex Tsariounov <alext@manetu.com>

This is free software; please see the LICENSE file
for details and any restrictions.
"""

def cmd_resolve(item, choices):
    candidates = [cmd for cmd in choices if cmd.startswith(item)]

    if not candidates:
        raise ValueError(f'unknown command: "{item}"')
    elif len(candidates) > 1:
        raise ValueError(f'ambiguous command: "{item}", candidates: "{candidates}"')

    return candidates[0]
