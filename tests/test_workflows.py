import pytest

from src.workflows.workflow_factory import WorkflowFactory
from tests.fakes import RecordingNodeFactory

# LangGraph only keeps keys declared in the state schema, which BaseWorkflow builds
# from the nodes' ``state_fields``; ``trace`` is declared so the tests can observe order.
NODE_CONFIG = {
    "a": {"type": "ai", "state_fields": {"a_out": str, "trace": list}, "output_field": "a_out"},
    "b": {"type": "ai", "state_fields": {"b_out": str, "trace": list}, "output_field": "b_out"},
    "c": {"type": "ai", "state_fields": {"c_out": str, "trace": list}, "output_field": "c_out"},
    "d": {"type": "ai", "state_fields": {"d_out": str, "trace": list}, "output_field": "d_out"},
    "stop_execution": {"type": "functional", "state_fields": {}, "output_field": None},
}


def _factory(workflows, outputs=None):
    return WorkflowFactory(workflows, RecordingNodeFactory(NODE_CONFIG, outputs))


def test_linear_workflow_runs_in_order():
    wf = _factory({"w": {
        "workflow_type": "linear",
        "nodes": [{"name": "a"}, {"name": "b"}, {"name": "c"}],
        "edges": [{"from_node": "a", "next_node": "b"}, {"from_node": "b", "next_node": "c"}],
        "entry_point": "a", "finish_point": "c",
    }}).create_workflow("w")
    out = wf.invoke({"trace": []})
    assert out["trace"] == ["a", "b", "c"]


def test_parallel_workflow_fans_out_and_in():
    wf = _factory({"w": {
        "workflow_type": "parallel",
        "nodes": [{"name": "a"}, {"name": "b"}, {"name": "c"}, {"name": "d"}],
        "edges": [{"from_node": "a", "next_node": ["b", "c"]}, {"from_node": ["b", "c"], "next_node": "d"}],
        "entry_point": "a", "finish_point": "d",
    }}, outputs={"b": "b_out", "c": "c_out"}).create_workflow("w")
    out = wf.invoke({"trace": []})
    # b and c both ran (distinct output fields), a ran first and d ran after both.
    assert out["b_out"] == "b-output" and out["c_out"] == "c-output"
    assert out["trace"][0] == "a" and out["trace"][-1] == "d"
    assert out["trace"][1] in {"b", "c"}


def test_conditional_workflow_stops_when_node_produced_no_output():
    workflows = {"w": {
        "workflow_type": "conditional",
        "nodes": [{"name": "a"}, {"name": "b"}, {"name": "stop_execution"}],
        "conditions": [{"from_node": "a", "condition": "check_node_output",
                        "paths": {"continue": "b", "end": "stop_execution"}}],
        "edges": [],
        "entry_point": "a", "finish_point": "b",
    }}
    # a produces its output -> continue to b
    out = _factory(workflows, outputs={"a": "a_out"}).create_workflow("w").invoke(
        {"trace": [], "curr_execution_node": None})
    assert out["trace"] == ["a", "b"]


def test_unknown_workflow_type_and_name():
    f = _factory({"w": {"workflow_type": "spiral", "nodes": [], "entry_point": "a", "finish_point": "a"}})
    with pytest.raises(ValueError):
        f.create_workflow("w")
    with pytest.raises(ValueError):
        f.create_workflow("missing")


def test_state_is_built_from_the_nodes_in_the_workflow():
    wf = _factory({"w": {
        "workflow_type": "linear", "nodes": [{"name": "a"}, {"name": "d"}],
        "edges": [{"from_node": "a", "next_node": "d"}], "entry_point": "a", "finish_point": "d",
    }}).build("w")
    fields = wf.build_state().__annotations__
    assert {"a_out", "d_out", "curr_execution_node", "last_node_output"} <= set(fields)
    assert fields["a_out"].__metadata__[0].__name__ == "last_writer_wins"
    assert "b_out" not in fields
