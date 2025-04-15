import psycopg

from src.entities.config import DatabaseConfig
from src.engine import AbstractDatabaseEngine


class PostgresEngine(AbstractDatabaseEngine):
    """Postgres engine"""

    def __init__(self, config: DatabaseConfig):
        super().__init__(config)
        self.connection_string = self.create_connection_string()

    def create_connection_string(self):
        """Method to create a connection string."""
        conn_string = (
            f"postgresql://{self.config.user}:{self.config.password}@"
            f"{self.config.host}:{self.config.port}/{self.config.name}"
        )
        return conn_string

    def connect(self):
        """Create a synchronous database connection."""
        try:
            return psycopg.connect(self.connection_string)
        except psycopg.OperationalError as e:
            raise RuntimeError(f"Failed to connect to the database: {e}")

    @staticmethod
    def get_data_type_mapping(field_type: str) -> str:
        """
        Maps a field to its corresponding PostgreSQL data type.
        If the schema defines the type, use it. Otherwise, infer the type from Python.
        """
        type_mapping = {
            # client side schema mapping
            "string": "TEXT",
            "boolean": "BOOLEAN",
            "integer": "INTEGER",
            "double": "FLOAT",
            "serial": "SERIAL",
            # Python type to PostgreSQL type mapping
            "int": "INTEGER",
            "str": "TEXT",
            "float": "FLOAT",
            "bool": "BOOLEAN",
            "datetime": "TIMESTAMP",
            # other types
            "default": "TEXT",
            "uuid": "UUID",
            "primary_key": "PRIMARY KEY",
        }
        data_type = type_mapping.get(field_type)
        return data_type

    def execute(self, query: str, *args):
        """
        Execute a SQL query synchronously.
        """
        try:
            with self.connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, args)
                    conn.commit()
        except Exception as e:
            raise RuntimeError(f"Failed to execute query. Error: {e}")

    def execute_with_values(self, query: str, values: tuple):
        """
        Execute a query with parameterized values.
        """
        try:
            with self.connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, values)
                    conn.commit()
        except Exception as e:
            raise RuntimeError(f"Failed to execute query with values. Error: {e}")

    def fetch(self, query: str, *args):
        """
        Fetch data from the database using a SQL query.

        Args:
            query (str): SQL query.
            *args: Query parameters.

        Returns:
            list: Query result rows.
        """
        try:
            with self.connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, args)
                    data = cursor.fetchall()
                    return data
        except Exception as e:
            raise RuntimeError(f"Failed to fetch query results. Error: {e}")

    def fetch_with_headers(self, query: str, *args):
        """
        Fetch data from the database using a SQL query.

        Args:
            query (str): SQL query.
            *args: Query parameters.

        Returns:
            list: Query result rows with column names.
        """
        try:
            with self.connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, args)

                    # Get column names from cursor.description
                    column_names = [desc[0] for desc in cursor.description]

                    # Fetch all rows of data
                    data = cursor.fetchall()

                    # Combine column names and rows of data (returning as list of dictionaries)
                    result = [dict(zip(column_names, row)) for row in data]

                    return result  # Returning list of dictionaries with column names as keys
        except Exception as e:
            raise RuntimeError(f"Failed to fetch query results. Error: {e}")

    def check_if_table_exists_query(self, table_name: str):
        """
        Check if a table exists.
        :param table_name: Name of the table to check
        """
        check_query = f"""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables 
                WHERE table_name = {table_name}
            );
        """
        return check_query