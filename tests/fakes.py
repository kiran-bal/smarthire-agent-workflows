"""Stand-ins for the CrewAI-backed factories so graph wiring can be tested without a model."""


class FakeLLM:
    def __init__(self, reply="fake reply"):
        self.reply = reply
        self.prompts = []

    def call(self, prompt):
        self.prompts.append(prompt)
        return self.reply


class FakeAgentFactory:
    def __init__(self, config=None, llm=None):
        self.config = config or {}
        self.llm = llm or FakeLLM()


class FakeTaskFactory:
    def __init__(self, config=None):
        self.config = config or {}


class RecordingNode:
    """Minimal node whose execute() appends its name to state['trace']."""

    def __init__(self, name, output_field=None):
        self.name = name
        self.output_field = output_field

    def execute(self, state):
        state = dict(state)
        state["prev_execution_node"] = state.get("curr_execution_node")
        state["curr_execution_node"] = self.name
        state["trace"] = list(state.get("trace") or []) + [self.name]
        if self.output_field:
            state[self.output_field] = f"{self.name}-output"
        return state


class RecordingNodeFactory:
    """Duck-types NodeFactory: has .config and create_node()."""

    def __init__(self, config, outputs=None):
        self.config = config
        self.outputs = outputs or {}

    def create_node(self, node_name, node_config):
        return RecordingNode(node_name, self.outputs.get(node_name))
