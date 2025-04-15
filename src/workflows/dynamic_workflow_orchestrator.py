import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
# from langchain_ollama.chat_models import ChatOllama
from crewai import LLM

from src.agents.agent_factory import AgentFactory
from src.nodes.node_factory import NodeFactory
from src.tasks.task_factory import TaskFactory
from src.tools.tool_factory import ToolFactory
from src.workflows.workflow_factory import WorkflowFactory

load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")
# model = "gpt-4o-mini"
# llm = ChatOpenAI(model=model, api_key=api_key, temperature=0.5, streaming=True)

llm = LLM(
        model="ollama/deepseek-r1:7b",
        temperature=0.5,
        base_url="http://localhost:11434"
)

# llm = ChatGroq(
#     model='groq/llama-3.3-70b-versatile',
#     api_key=os.environ.get("GROQ_API_KEY"),
#     temperature=0.5,
#     max_tokens=500,
#     streaming=True
# )

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
