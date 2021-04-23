"""GraphQL interface"""

__copyright__ = """
Copyright (C) 2021 Manetu Inc.
Author: Alex Tsariounov <alext@manetu.com>

This is free software; please see the LICENSE file
for details and any restrictions.
"""

import urllib.parse, urllib.request
from urllib.error import URLError

class GQL(object):
    """GraphQL server encapsulating class"""

    def __init__(self, headers, uri, verbosity):
        """constructor with a dict as headers and a uri pointing to the server"""
        self.headers = headers
        self.uri = uri
        self.verbosity = verbosity

    def query(self, query, variables):
        """takes a json query and a variables dict (if any) as parameters, returns json_data, raises if status is bad, or other error"""

        #data = urllib.parse.urlencode(query)
        data = query.encode('utf-8') # encode to bytes
        request = urllib.request.Request(self.uri, data, self.headers)
        request.add_header('Content-Type', 'application/json; charset=utf-8')
        request.add_header('Content-Length', len(data))
        
        try:
            with urllib.request.urlopen(request) as response:
                page = response.read()
        except URLError as e:
            if self.verbosity > 0:
                if hasattr(e, 'reason'):
                    print(f"Can't reach server {self.uri} because: {e.reason}")
                elif hasattr(e, 'code'):
                    print(f"Server error (code: {e.code}): {e.msg}")
            raise e

        return str(page)

    def mutation(self, command):
        pass
