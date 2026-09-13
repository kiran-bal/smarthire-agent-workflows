"""
Builds the factory chain (tools -> agents -> tasks -> nodes -> workflows) for a
request-supplied configuration. The LLM is chosen from the environment:

    LLM_PROVIDER=ollama   LLM_MODEL=llama3.1          (default)
    LLM_PROVIDER=openai   LLM_MODEL=gpt-4o-mini       OPENAI_API_KEY=...
    LLM_PROVIDER=groq     LLM_MODEL=llama-3.3-70b-versatile  GROQ_API_KEY=...
"""

import os

from dotenv import load_dotenv
from crewai import LLM

from src.agents.agent_factory import AgentFactory
from src.nodes.node_factory import NodeFactory
from src.tasks.task_factory import TaskFactory
from src.tools.tool_factory import ToolFactory
from src.workflows.workflow_factory import WorkflowFactory

load_dotenv()


def build_llm() -> LLM:
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()
    model = os.getenv("LLM_MODEL", "llama3.1")
    temperature = float(os.getenv("LLM_TEMPERATURE", "0.5"))
    if provider == "ollama":
        return LLM(
            model=f"ollama/{model}",
            temperature=temperature,
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        )
    if provider == "openai":
        return LLM(model=model, temperature=temperature, api_key=os.getenv("OPENAI_API_KEY"))
    if provider == "groq":
        return LLM(model=f"groq/{model}", temperature=temperature, api_key=os.getenv("GROQ_API_KEY"))
    raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")


llm = build_llm()


class DynamicWorkflowOrchestrator:
    """
    Orchestrator class for the workflows
    """

    def __init__(self):
        self.config = None

    def get_workflow_factory(self, config: dict):
        """
        Creates and returns the workflow factory
        Returns:
            WorkflowFactory: Object of the workflow factory
        """
        self.config = config

        tool_factory = ToolFactory(config=self.config.get("tools"))
        agent_factory = AgentFactory(
            config=self.config.get("agents"), llm=llm, tool_factory=tool_factory
        )
        task_factory = TaskFactory(
            config=self.config.get("tasks"), agent_factory=agent_factory
        )

        node_factory = NodeFactory(
            config=self.config.get("nodes"),
            agent_factory=agent_factory,
            task_factory=task_factory,
        )

        workflow_factory = WorkflowFactory(
            config=self.config.get("workflow"), node_factory=node_factory
        )

        return workflow_factory
