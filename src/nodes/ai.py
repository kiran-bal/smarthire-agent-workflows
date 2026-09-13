"""
Direct LLM node: renders a prompt template from the workflow state, calls the
configured LLM once, and stores the reply in the node's output field.

Use it for steps that do not need a crew (classification, extraction,
rewriting). Node configuration:

    summarise_resume:
      type: ai
      prompt: "Summarise this resume in three bullet points:\n{pdf_text_extract_output}"
      state_fields:
        resume_summary: str
      output_field: resume_summary
"""

from constants import CURR_EXECUTION_NODE_KEY, LAST_NODE_OUTPUT_KEY, PREV_EXECUTION_NODE_KEY
from src.nodes.base import BaseNode


class AINode(BaseNode):
    """
    Creates and executes single-call LLM nodes.
    """

    def __init__(self, config, agent_factory, task_factory, node_name):
        super().__init__(config, agent_factory, task_factory)
        self.node_name = node_name

    @staticmethod
    def call_llm(llm, prompt: str) -> str:
        """Support crewai.LLM (``call``) and LangChain chat models (``invoke``)."""
        if hasattr(llm, "call"):
            return str(llm.call(prompt))
        result = llm.invoke(prompt)
        return str(getattr(result, "content", result))

    def execute(self, state):
        node_config = self.config.get(self.node_name)
        if not node_config:
            raise ValueError(f"Node {self.node_name} not found in configuration.")
        template = node_config.get("prompt")
        if not template:
            raise ValueError(f"AI node {self.node_name} needs a 'prompt' template.")
        output_field = node_config.get("output_field")
        if not output_field:
            raise ValueError(f"AI node {self.node_name} needs an 'output_field'.")

        state[PREV_EXECUTION_NODE_KEY] = state.get(CURR_EXECUTION_NODE_KEY)
        state[CURR_EXECUTION_NODE_KEY] = self.node_name
        inputs = {**state, **(node_config.get("inputs") or {})}
        prompt = template.format(**inputs)
        reply = self.call_llm(self.agent_factory.llm, prompt)
        state[LAST_NODE_OUTPUT_KEY] = reply
        state[output_field] = reply
        return state
