from collections import defaultdict

from src.adapters.base import AbstractWorkflowAdapter


class CustomConditionalAdapter(AbstractWorkflowAdapter):

    def __init__(self):
        """
        Initialize the Workflow Adapter with configuration and request structure.
        """
        super().__init__()
        self.config = None  # Workflow config with node templates
        self.source_config = None
        self.workflow_config = dict()  # Final workflow configuration
        self.updated_nodes = {}  # Updated nodes after processing

    def adapt_workflow(self, source_config):
        """
        Adapt the workflow by matching nodes, updating inputs, and linking nodes.
        :return: The fully adapted workflow configuration with updated nodes and inputs.
        """
        self.source_config = source_config
        self.config = {'nodes': self.config_manager.get("nodes")}
        sequence_content = self.source_config['sequenceContent']
        first_block = sequence_content['firstBlock']
        blocks = sequence_content['blocks']

        # Process the blocks and update inputs
        node_mapping = {block['blockId']: block for block in blocks}
        current_block = node_mapping.get(first_block)

        while current_block:
            node_template = self.get_node_template(current_block['blockType'])
            if node_template:
                updated_node = self.update_node_inputs(node_template, current_block)
                self.updated_nodes[updated_node["blockType"]] = updated_node

            # Move to the next block
            next_block_id = current_block.get('next')
            current_block = node_mapping.get(next_block_id) if next_block_id != "End" else None

        # Create the final workflow configuration
        self.create_workflow_config()
        dynamic_workflow = {"dynamic_workflow": self.workflow_config}

        config = {
            "agents": self.config_manager.get("agents"),
            "tools": self.config_manager.get("tools"),
            "tasks": self.config_manager.get("tasks"),
            "nodes": self.updated_nodes,
            "workflow": dynamic_workflow
        }

        return config

    def validate_request_structure(self):
        """
        Abstract method to validate the request structure.
        Can be customized per adapter type.
        """
        pass

    def get_node_template(self, block_type):
        """
        Retrieve the node template from the configuration using the block type.
        """
        return self.config.get('nodes', {}).get(block_type, None)

    def update_node_inputs(self, node_template, block):
        """
        Update the node's inputs using the userMeta from the block.
        """
        updated_inputs = {}
        node_template_inputs = node_template.get("inputs")
        node_template_inputs = node_template_inputs if node_template_inputs else {}
        for input_field, input_type in node_template_inputs.items():
            updated_inputs[input_field] = block['userMeta'].get(input_field, None)
        node_template['inputs'] = updated_inputs
        node_template['blockId'] = block['blockId']
        node_template['blockName'] = block['blockName']
        node_template['blockType'] = block['blockType']
        return node_template

    def create_workflow_config(self):
        """
        Create the final workflow configuration including nodes and edges.
        """
        self.workflow_config['workflow_type'] = 'conditional'

        nodes_list = [
            {
                "id": node["blockType"],
                "type": node["type"],
                "name": node["blockType"],
            }
            for node in self.updated_nodes.values()
        ]

        self.workflow_config['nodes'] = nodes_list

        # Create edges for the workflow
        # Create edges based on the ordered nodes
        nodes_ordered = list(self.updated_nodes.values())

        edges = [
            {
                "from_node": nodes_ordered[i]["blockType"],
                "condition": "check_node_output",
                "paths": {
                    "continue": nodes_ordered[i + 1]["blockType"],
                    "end": "stop_execution"
                }} for i in range(len(nodes_ordered) - 1)
        ]
        self.workflow_config['conditions'] = edges

        # Add entry and finish points
        self.workflow_config["entry_point"] = nodes_ordered[0]["blockType"] if nodes_ordered else None
        self.workflow_config["finish_point"] = nodes_ordered[-1]["blockType"] if nodes_ordered else None
