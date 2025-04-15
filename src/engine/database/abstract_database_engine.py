from abc import ABC, abstractmethod

from src.entities.config import DatabaseConfig


class AbstractDatabaseEngine(ABC):
    """Abstract DB Engine"""

    def __init__(self, config: DatabaseConfig):
        """
        Initialize the database engine with configuration.
        :param config: Dictionary containing database configuration
        """
        self.config = config

    @abstractmethod
    def create_connection_string(self):
        """Method to create a connection string."""
        pass

    def connect(self):
        """Create a synchronous database connection."""
        pass

    @staticmethod
    @abstractmethod
    def get_data_type_mapping(field_type: str):
        """
        Maps a field to its corresponding SQL data type.
        If the schema defines the type, use it. Otherwise, infer the type from Python.
        """
        pass

    @abstractmethod
    def execute(self, query: str, *args):
        """
        Execute a given SQL query.
        :param query: SQL query string
        :param args: Query parameters
        """
        pass

    @abstractmethod
    def execute_with_values(self, query: str, values: tuple):
        """
        Execute a query with parameterized values.
        """
        pass

    @abstractmethod
    def fetch(self, query: str, *args):
        """
        Fetch data from the database using a SQL query.

        Args:
            query (str): SQL query.
            *args: Query parameters.

        Returns:
            list: Query result rows.
        """