"""
Contains Factory class to create tools
"""

from constants import *
from src.tools.notification.send_gmail import gmail_send_tool
from src.tools.report.pdf_text_extract import pdf_text_extract_tool

from src.tools.web.web_rag_search_tool import web_rag_search_tool
from src.tools.sheets.csv_rag_search_tool import csv_rag_search_tool


# Tool Factory
class ToolFactory:
    """
    Creates tools based on configuration
    """

    def __init__(self, config):
        self.config = config

    def create_tool(self, name: str, inputs: dict):
        """
        Creates tools based on the given name. the tool must be in the
        configuration
        Args:
            name: unique name of the tool
            inputs: list of inputs required for the tool
        Returns:
            created tool based on configuration
        """
        tool_config = self.config.get(name)
        tool_config_inputs = tool_config["inputs"] if tool_config.get("inputs") else {}
        tool_inputs = {
            target_key: inputs.get(source_key, None)
            for source_key, target_key in tool_config_inputs.items()
        }
        if not tool_config:
            raise ValueError(f"Tool {name} not found in configuration.")

        if name == CREW_WEB_RAG_SEARCH_TOOL:
            return web_rag_search_tool(**tool_inputs)
        elif name == CREW_CSV_SEARCH_TOOL:
            return csv_rag_search_tool(**tool_inputs)
        elif name == CREW_PDF_TEXT_EXTRACTION_TOOL:
            return pdf_text_extract_tool()
        elif name == CREW_SEND_GMAIL_TOOL:
            return gmail_send_tool()

        # Add other tool initializations as needed
        return None
