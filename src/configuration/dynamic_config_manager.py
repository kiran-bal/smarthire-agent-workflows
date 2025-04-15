import yaml
from typing import Dict, Any

class DynamicConfigManager:
    def __init__(
            self, tool_config_path:str,
            agent_config_path: str,
            task_config_path: str,
            crew_config_path: str
    ):

        self.config_paths = {
            "tools": tool_config_path,
            "agents": agent_config_path,
            "tasks": task_config_path,
            "nodes": crew_config_path
        }
        self.config = self._load_configurations()

    @staticmethod
    def _load_yaml(path: str) -> Dict[str, Any]:
        with open(path, "r") as file:
            return yaml.safe_load(file)

    def _load_configurations(self) -> Dict[str, Any]:
        return {key: self._load_yaml(path) for key, path in self.config_paths.items()}

    def get(self, config_name: str) -> Dict[str, Any]:
        return self.config.get(config_name, {})
