"""
Contains the class to create and execute the crew nodes
"""

import json
from typing import Any
from crewai import Crew

from src.entities.states import WorkflowGraphState
from src.nodes.base import BaseNode
from constants import CREW_TASKS_KEY, CURR_EXECUTION_NODE_KEY, PREV_EXECUTION_NODE_KEY, LAST_NODE_OUTPUT_KEY
from utils.log_message import custom_log


class CrewNode(BaseNode):
    """
    Creates and executes crew nodes
    """

    def __init__(self, config, agent_factory, task_factory, node_name):
        super().__init__(config, agent_factory, task_factory)
        self.node_name = node_name


    def __create_crew(self) -> Crew:
        """
        Creates the crew based on the given configuration
        agents and tasks will be created based on the configuration
        Returns:
            Crew: created crew with the help of configuration
        """
        crew_config = self.config.get(self.node_name)
        inputs = crew_config.get("inputs")
        if not crew_config:
            raise ValueError(f"Crew {self.node_name} not found in configuration.")

        tasks = []
        for task_name in crew_config.get(CREW_TASKS_KEY, []):
            task = self.task_factory.create_task(task_name, inputs=inputs)
            tasks.append(task)

        tasks = [
            self.task_factory.create_task(task_name, inputs=inputs, tasks=tasks)
            for task_name in crew_config.get(CREW_TASKS_KEY, [])
        ]
        agents = [task.agent for task in tasks]

        return Crew(agents=agents, tasks=tasks, verbose=True)

    def execute(self, state: dict[str, Any]) -> WorkflowGraphState:
        """
        Executes the crew node and saves the state information
        Args:
            state: lang graph state for current execution

        Returns:
            WorkflowGraphState: Updated lang graph state for current execution
        """
        state[PREV_EXECUTION_NODE_KEY] = state.get(CURR_EXECUTION_NODE_KEY)
        state[CURR_EXECUTION_NODE_KEY] = self.node_name
        crew_config = self.config.get(self.node_name)
        # TODO: Update here for node execution
        inputs = crew_config.get("inputs")
        inputs = inputs if inputs else {}

        crew = self.__create_crew()
        node_config = self.config.get(self.node_name)
        node_output_field = node_config.get("output_field")
        custom_log(f"### Kicking off crew: {self.node_name}")
        state = {**state, **inputs}
        state[LAST_NODE_OUTPUT_KEY] = state[LAST_NODE_OUTPUT_KEY] if LAST_NODE_OUTPUT_KEY in state else ""
        result = crew.kickoff(inputs=state)

        # result = crew.kickoff(inputs={**state, **inputs})
        state[LAST_NODE_OUTPUT_KEY] = result.raw

        node_output_field_type = node_config.get("state_fields")[node_output_field]
        if node_output_field_type == 'dict':
            state[node_output_field] = json.loads(result.raw)
        else:
            state[node_output_field] = result.raw
        return state
