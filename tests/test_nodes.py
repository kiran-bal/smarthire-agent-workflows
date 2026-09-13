import pytest

from src.nodes.ai import AINode
from src.nodes.node_factory import NodeFactory
from tests.fakes import FakeAgentFactory, FakeLLM, FakeTaskFactory

NODES = {
    "summary": {"type": "ai", "prompt": "Summarise: {resume_text}", "output_field": "summary",
                "state_fields": {"summary": "str"}},
    "extract": {"type": "crew", "agents": ["x"], "tasks": ["t"], "output_field": "resume_text",
                "state_fields": {"resume_text": "str"}},
}


def test_factory_builds_each_type_and_rejects_unknown():
    f = NodeFactory(NODES, FakeAgentFactory(), FakeTaskFactory())
    assert isinstance(f.create_node("summary", NODES["summary"]), AINode)
    assert f.create_node("extract", NODES["extract"]).__class__.__name__ == "CrewNode"
    with pytest.raises(ValueError):
        f.create_node("bad", {"type": "teleport"})


def test_ai_node_renders_prompt_and_stores_reply():
    llm = FakeLLM(reply="three bullets")
    node = AINode(NODES, FakeAgentFactory(llm=llm), FakeTaskFactory(), "summary")
    state = node.execute({"resume_text": "10 years of Python", "curr_execution_node": "extract"})
    assert llm.prompts == ["Summarise: 10 years of Python"]
    assert state["summary"] == "three bullets"
    assert state["last_node_output"] == "three bullets"
    assert state["prev_execution_node"] == "extract"
    assert state["curr_execution_node"] == "summary"


def test_ai_node_requires_prompt_and_output_field():
    cfg = {"n": {"type": "ai", "output_field": "o"}}
    with pytest.raises(ValueError):
        AINode(cfg, FakeAgentFactory(), FakeTaskFactory(), "n").execute({})
    cfg = {"n": {"type": "ai", "prompt": "hi"}}
    with pytest.raises(ValueError):
        AINode(cfg, FakeAgentFactory(), FakeTaskFactory(), "n").execute({})


def test_ai_node_supports_langchain_style_llms():
    class Reply:
        content = "from invoke"

    class LCModel:
        def invoke(self, prompt):
            return Reply()

    assert AINode.call_llm(LCModel(), "x") == "from invoke"
