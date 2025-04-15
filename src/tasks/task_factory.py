"""
Contains the class to create tasks
"""

from crewai import Task

from constants import (
    CREW_TASK_DESCRIPTION_KEY,
    CREW_TASK_EXP_OUTPUT_KEY,
    CREW_AGENT_KEY, CREW_TASK_CONTEXT_KEY, CREW_TASK_NAME_KEY
)


class TaskFactory:
    """
    Creates the tasks with given configuration and agent
    """

    def __init__(self, config, agent_factory):
        self.config = config
        self.agent_factory = agent_factory

    def create_task(self, name: str, inputs, tasks: list = []) -> Task:
        """
        Creates the task based on given name. the name should
        be in the task configuration.
        Args:
            name: unique name for the task
            inputs: inputs for the task
            tasks: list of tasks created
        Returns:
            Task: created task based on the configuration
        """
        task_config = self.config.get(name)
        if not task_config:
            raise ValueError(f"Task {name} not found in configuration.")
        agent = self.agent_factory.create_agent(task_config.get(CREW_AGENT_KEY), inputs)
        # context_list = task_config.get(CREW_TASK_CONTEXT_KEY, [])

        # context_task_list = []
        # for each_task in tasks:
        #     if each_task.name in context_list:
        #         context_task_list.append(each_task)

        task = Task(
            name=name,
            description=task_config.get(CREW_TASK_DESCRIPTION_KEY),
            expected_output=task_config.get(CREW_TASK_EXP_OUTPUT_KEY),
            agent=agent
            # context= context_task_list
        )
        return task
