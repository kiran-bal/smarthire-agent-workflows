import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional


class TemplateManager:
    """
    A manager class to load and manage multiple YAML configuration files.
    """

    def __init__(self) -> None:
        """
        Initialize the ConfigurationManager

        """
        pass

    @staticmethod
    def load_yaml_file(file_path: str) -> Optional[Dict[str, Any]]:
        """
        Load and parse a single YAML file.

        Args:
            file_path (str): Path to the YAML file.

        Returns:
            Optional[Dict[str, Any]]: Parsed content of the YAML file as a dictionary,
            or None if an error occurs.
        """
        try:
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file {file_path}: {e}")
        return None

    def load_all_configs(self, config_files: Dict[str, str]) -> Dict[str, Any]:
        """
        Load and combine configurations from all specified YAML files.

        Returns:
            Dict[str, Any]: Combined configuration as a dictionary.
        """
        combined_config = {}
        for key, file_path in config_files.items():
            config = self.load_yaml_file(file_path)
            if config:
                combined_config[key] = config
            else:
                combined_config[key] = None  # Optional: Set None if the file couldn't be loaded
        return combined_config


