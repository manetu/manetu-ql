"""GraphQL: get all subscriptions and their attributes"""

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
    subscriptionType {
        ...FullType
    }
  }
}
"""

queryShort = """
{
  __schema {
    subscriptionType {
      fields {
        name
        description
      }
    }
  }
}
"""
