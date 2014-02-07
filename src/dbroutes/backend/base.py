import re

from django.db.backends.postgresql_psycopg2.base import *

# from the postgresql doc
SQL_IDENTIFIER_RE = re.compile(r'^[_a-zA-Z][_a-zA-Z0-9]{,62}$')

PUBLIC_SCHEMA_NAME = 'public'


def _check_identifier(identifier):
    if not SQL_IDENTIFIER_RE.match(identifier):
        raise RuntimeError("Invalid string used for the schema name.")


class DatabaseWrapper(DatabaseWrapper):
    """
    Adds the capability to manipulate the search_path using set_schema_name.
    """
    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        self.set_schema(self.settings_dict.get('SCHEMA', PUBLIC_SCHEMA_NAME))

    def set_schema(self, schema_name, include_public=True):
        self.schema_name = schema_name
        self.include_public_schema = include_public

    def set_schema_to_public(self):
        self.schema_name = PUBLIC_SCHEMA_NAME

    def _cursor(self):
        cursor = super(DatabaseWrapper, self)._cursor()

        if not self.schema_name:
            raise ValueError(
                "Database schema not set. Did your forget to call set_schema()?")

        _check_identifier(self.schema_name)
        if self.schema_name == PUBLIC_SCHEMA_NAME:
            schemas = [PUBLIC_SCHEMA_NAME]
        elif self.include_public_schema:
            schemas = [self.schema_name, PUBLIC_SCHEMA_NAME]
        else:
            schemas = [self.schema_name]

        query = 'SET search_path = %s' % (','.join('%s' for _ in schemas),)
        cursor.execute(query, schemas)

        return cursor
