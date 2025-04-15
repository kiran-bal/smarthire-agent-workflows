"""
Contains factory class to build the agents based on configuration
"""

from crewai import Agent

from constants import (
    CREW_AGENT_GOAL_KEY,
    CREW_TOOLS_KEY,
    CREW_AGENT_ROLE_KEY,
    CREW_AGENT_BACKGROUND_KEY,
)


class AgentFactory:
    """
    Factory class to build the agents based on configuration
    """

    def __init__(self, config, llm, tool_factory):
        self.config = config
        self.llm = llm
        self.tool_factory = tool_factory

    def create_agent(self, name: str, inputs: dict) -> Agent:
        """
        Creates the agent based on the configuration
        Args:
            name: name of the agent to be created
            this name and details must be there in the agents configuration
            inputs: inputs required for the agent or tools if any

        Returns:
            Agent: created agent based on the configuration
        """
        agent_config = self.config.get(name)
        if not agent_config:
            raise ValueError(f"Agent {name} not found in configuration.")

        tools = [
            self.tool_factory.create_tool(tool_name, inputs=inputs)
            for tool_name in agent_config.get(CREW_TOOLS_KEY, [])
        ]

        # Initialize and return the agent based on the configuration
        agent = Agent(
            role=agent_config.get(CREW_AGENT_ROLE_KEY),
            goal=agent_config.get(CREW_AGENT_GOAL_KEY),
            backstory=agent_config.get(CREW_AGENT_BACKGROUND_KEY),
            tools=tools,
            verbose=True,
            max_iter=5,
            max_retry_limit=2,
            llm=self.llm
        )
        return agent
