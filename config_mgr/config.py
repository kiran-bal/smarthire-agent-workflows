import os

from constants import *
from src.constants import *
from src.entities.config import DatabaseConfig
from utils.util import read_yaml
from entity.config_entity import *


class Configuration:
    """Configuration

    Args:
        config_file_name (str, optional): path pointing to application configuration yaml file.
                                          Defaults to CONFIG_FILE_PATH.
    """

    def __init__(
        self,
        config_file_name: str = APPLICATION_CONFIG_FILE_NAME
    ) -> None:
        """Configuration Constructor"""
        self.app_config = read_yaml(config_file_name)

    def _get_config(self, config_file_name: str) -> None:
        """method to retrieve the configurations

        Args:
            config_file_name (str): config file name

        Returns:
            Config: Loaded Config
        """
        pass

    @staticmethod
    def get_dynamic_config(env_var, app_config_attr) -> str:
        """Load env from dot env by default if it exists"""
        config = os.getenv(env_var) or app_config_attr
        return config

    @staticmethod
    def get_agents_config() -> AgentsConfig:
        """Retrieve the agents configuration"""
        agents_config = read_yaml(file_name=AGENTS_CONFIG_FILENAME)
        agent_tools_config = read_yaml(file_name=AGENT_TOOLS_FILENAME)
        agent_category_config = read_yaml(file_name=AGENT_CATEGORY_FILENAME)
        agent_config = AgentsConfig(
            agent_category_config=agent_category_config,
            agents_config=agents_config,
            agent_tools_config=agent_tools_config
        )
        return agent_config

    def get_database_config(self) -> DatabaseConfig:
        """Database configurations

        Returns:
            DatabaseConfig
        """
        db_config = self.app_config.database
        dialect = self.get_dynamic_config(
            DB_DIALECT, db_config.dialect
        )
        host = self.get_dynamic_config(
            DB_HOST, db_config.host
        )
        port = self.get_dynamic_config(
            DB_PORT, db_config.port
        )
        name = self.get_dynamic_config(
            DB_NAME, db_config.name
        )
        user = self.get_dynamic_config(
            DB_USER, db_config.user
        )
        password = self.get_dynamic_config(
            DB_PASSWORD, db_config.password
        )
        db_config = DatabaseConfig(
            dialect=dialect,
            host=host,
            port=port,
            name=name,
            user=user,
            password=password
        )
        return db_config