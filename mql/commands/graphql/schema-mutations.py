"""GraphQL: get all mutations and thier attributes"""

__copyright__ = """
Copyright (C) 2021 Manetu Inc.
Author: Alex Tsariounov <alext@manetu.com>

This is free software; please see the LICENSE file
for details and any restrictions.
"""

from mql.commands.graphql.fragments import FullType

queryFull = FullType + """
query IntrospectionQuery {
  __schema {
    mutationType {
        ...FullType
    }
  }
}
"""

queryShort = """
{
  __schema {
    mutationType {
      fields {
        name
        description
      }
    }
  }
}
"""
