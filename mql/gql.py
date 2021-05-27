"""GraphQL interface"""

__copyright__ = """
Copyright (C) 2021 Manetu Inc.
Author: Alex Tsariounov <alext@manetu.com>

This is free software; please see the LICENSE file
for details and any restrictions.
"""

import json, time, urllib.parse, urllib.request, http.client
from urllib.error import URLError

class GQL(object):
    """GraphQL server encapsulating class"""

    def __init__(self, headers, uri, verbosity):
        """constructor with a dict as headers and a uri pointing to the server"""
        self.headers = headers
        self.uri = uri
        self.verbosity = verbosity

    def __send_command(self, data):
        """send actual data command, return decoded body"""
        request = urllib.request.Request(self.uri, data, self.headers)
        request.add_header('Content-Type', 'application/json; charset=utf-8')
        request.add_header('Content-Length', len(data))
        if self.verbosity > 2:
            print(f'request.full_url: {request.full_url}')
            print(f'request.header_items: {request.header_items()}')
            print(f'request.data: {request.data}')

        try:
            attempts = 5
            for i in range(attempts):
                rsp = urllib.request.urlopen(request)
                try:
                    response = rsp.read()
                    if self.verbosity > 1:
                        print(f'read response in {i+1} tries')
                    break
                except http.client.IncompleteRead:
                    if i >= attempts-1:
                        if self.verbosity > 0:
                            print(f'incomplete read #{i+1} -> giving up')
                        raise
                    tm = i*3
                    if self.verbosity > 1:
                        print(f'incomplete read, wating {tm} seconds to retry...')
                    rsp.close()
                    time.sleep(tm)

        except URLError as e:
            if self.verbosity > 0:
                if hasattr(e, 'reason'):
                    print(f"Can't reach server {self.uri} because: {e.reason}")
                elif hasattr(e, 'code'):
                    print(f"Server error (code: {e.code}): {e.msg}")
                msg = e.read().decode()
                print(json.dumps(json.loads(msg), indent=2))
            raise e

        return response.decode('utf-8')

    def query(self, query, variables=None):
        """takes a json query and a variables dict (if any) as parameters, returns json_data, raises if status is bad, or other error"""
        if variables == None:
            data = json.dumps({'query': query}).encode('utf-8') # encode to bytes
        else:
            data = json.dumps({'query': query, 'variables': variables}).encode('utf-8')

        if self.verbosity > 2:
            print(f'using query: {data}')

        return self.__send_command(data)        

    def mutation(self, mutation, variables=None):
        """takes a json mutaions and a variables dict (if any) as parameters, returns json_data, raises if status is bad, or other error"""
        if variables == None:
            data = json.dumps({'mutation': mutation}).encode('utf-8') # encode to bytes
        else:
            data = json.dumps({'mutation': mutation, 'variables': variables}).encode('utf-8')

        if self.verbosity > 2:
            print(f'using mutation: {data}')

        return self.__send_command(data)
