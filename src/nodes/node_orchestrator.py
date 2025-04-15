import os
from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
from langchain_ollama.chat_models import ChatOllama

from src.agents.agent_factory import AgentFactory
from src.nodes.node_factory import NodeFactory
from src.tasks.task_factory import TaskFactory
from src.tools.tool_factory import ToolFactory
from src.configuration.dynamic_config_manager import DynamicConfigManager

load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")
# model = "gpt-4o-mini"
# llm = ChatOpenAI(model=model, api_key=api_key, temperature=0)

llm = ChatOllama(
        model="deepseek-r1:1.5b",
        temperature=0.3,
        base_url="http://localhost:11434"
)


class NodeOrchestrator:
    """
    Orchestrator class for the nodes
    """
    def __init__(self):
        config_manager = DynamicConfigManager(
            f"src/tools/tools_registry/tools.yaml",
            f"src/agents/agent_registry/agents.yaml",
            f"src/tasks/tasks_registry/tasks.yaml",
            f"src/nodes/nodes_registry/nodes.yaml"
        )

        # Retrieve configurations
        self.tool_configs = config_manager.get("tools")
        self.agent_configs = config_manager.get("agents")
        self.task_configs = config_manager.get("tasks")
        self.node_configs = config_manager.get("nodes")
        self.node_config = config_manager.get("node")

    def get_node_factory(self):
        """
        Creates and returns the node factory
        Returns:
            NodeFactory: Object of the node factory
        """
        tool_factory = ToolFactory(config=self.tool_configs)
        agent_factory = AgentFactory(
            config=self.agent_configs, llm=llm, tool_factory=tool_factory
        )
        task_factory = TaskFactory(
            config=self.task_configs, agent_factory=agent_factory
        )

        node_factory = NodeFactory(
            config=self.node_configs,
            agent_factory=agent_factory,
            task_factory=task_factory,
        )

        return node_factory
