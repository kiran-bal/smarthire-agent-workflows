import re
import time
import json
from typing import Optional

import pandas as pd

from constants import CURR_EXECUTION_NODE_KEY
from entity.config_entity import MailConfig
from src.managers.notifications.mail.sendgrid_manager import SendGridManager
from src.handlers.nodes.base import BaseNodeHandler
from utils.log_message import custom_log


# Add abstract class for the these
class QuotationNodeHandler(BaseNodeHandler):
    def __init__(self, config: dict, method = None):
        self.config = config
        self.method = method
        self.node_output_field = None
        super().__init__(config)

    def execute(self, state):
        if hasattr(self, self.method):
            func = getattr(self, self.method)
            curr_node = state.get(CURR_EXECUTION_NODE_KEY)
            self.node_output_field = self.config.get(curr_node, {}).get("output_field")
            state = func(state) if self.node_output_field else state
            return state
        raise AttributeError(f"Method '{self.method}' not found in {self.__class__.__name__}")

    def search_master_data_node(self, state):
        custom_log("### Executing the csv search node ###")

        sheet_id = state.get("master_sheet_id")
        sheet_name = state.get("master_sheet_tab_name")
        sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

        dict_format = []
        column_name = "Item No."
        lang_column_name = "Language"
        search_value = state.get("web_search_output", {}).get("sku_id")
        search_value = search_value.replace("-Legrand", "").strip() if search_value else ""
        # csv_path = state.get("master_csv_path")
        # df = pd.read_csv(csv_path)
        df = pd.read_csv(sheet_url)

        matched_row = df[df[column_name] == search_value]

        # Display the result
        if not matched_row.empty:
            custom_log("Matched row(s):")
            custom_log(matched_row)
            state["language"] = matched_row[lang_column_name].iloc[0]
            dict_format = matched_row.to_dict(orient='records')
            custom_log(json.dumps(dict_format))
        else:
            custom_log("No match found.")
        state[self.node_output_field] = dict_format
        return state

    def vashi_csv_search(self, state):

        custom_log("### Executing the csv search node ###")

        # sheet_id = state.get("master_sheet_id")
        tab_name = state.get("master_sheet_tab_name")
        sheet_url = state.get("sheet_url")
        sheet_id = self.extract_sheet_id(url=sheet_url)
        sheet_tool_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={tab_name}"

        dict_format = []
        column_name = "Item No."
        lang_column_name = "Language"
        search_value = state.get("web_search_output", {}).get("sku_id")
        search_value = search_value.replace("-Legrand", "").strip() if search_value else ""
        # csv_path = state.get("master_csv_path")
        # df = pd.read_csv(csv_path)
        df = pd.read_csv(sheet_tool_url)

        matched_row = df[df[column_name] == search_value]

        # Display the result
        if not matched_row.empty:
            custom_log("Matched row(s):")
            custom_log(matched_row)
            # TODO: Add new agent for language selection
            state["language"] = matched_row[lang_column_name].iloc[0]
            dict_format = matched_row.to_dict(orient='records')
            custom_log(json.dumps(dict_format))
        else:
            custom_log("No match found.")
        state[self.node_output_field] = dict_format
        return state

    def language_selection(self, state):

        custom_log("### Executing language selection node ###")

        sheet_id = state.get("master_sheet_id")
        sheet_name = state.get("master_sheet_tab_name")
        sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

        dict_format = []
        column_name = "Item No."
        lang_column_name = "Language"
        search_value = state.get("web_search_output", {}).get("sku_id")
        search_value = search_value.replace("-Legrand", "").strip() if search_value else ""
        # csv_path = state.get("master_csv_path")
        # df = pd.read_csv(csv_path)
        df = pd.read_csv(sheet_url)

        matched_row = df[df[column_name] == search_value]

        # Display the result
        if not matched_row.empty:
            custom_log("Matched row(s):")
            custom_log(matched_row)
            state["language"] = matched_row[lang_column_name].iloc[0]
            dict_format = matched_row.to_dict(orient='records')
            custom_log(json.dumps(dict_format))
        else:
            custom_log("No match found.")
        return dict_format

    def check_node_output(self, state):
        curr_execution_node = state.get(CURR_EXECUTION_NODE_KEY)
        curr_output_field = self.config[curr_execution_node].get("output_field")
        node_output = state.get(curr_output_field)
        if node_output:
            custom_log("## Node execution success")
            return "continue"
        else:
            custom_log("## No node execution result")
            return "end"


    @staticmethod
    def check_web_search_output(state):
        if state.get("web_search_output", {}).get("sku_id"):
            custom_log("## Web search success")
            return "continue"
        else:
            custom_log("## No web search result")
            return "end"

    @staticmethod
    def check_csv_search_output(state):
        if state.get("csv_search_output"):
            custom_log("## CSV search success")
            return "continue"
        else:
            custom_log("## No CSV search result")
            return "end"

    @staticmethod
    def check_offer_processor_output(state):
        if state.get("quote_final_output"):
            custom_log("## Offer Processing success")
            return "continue"
        else:
            custom_log("## No Offer processing result")
            return "end"

    @staticmethod
    def check_draft_output(state):
        if state.get("mail_draft_output"):
            custom_log("## Mail draft success")
            return "continue"
        else:
            custom_log("## No Mail draft result")
            return "end"

    @staticmethod
    def wait_next_run(state):
        custom_log("## Waiting for 180 seconds")
        time.sleep(180)
        return state

    @staticmethod
    def stop_execution(state):
        custom_log("## Stopping the current execution")
        return state

    @staticmethod
    def new_emails(state):
        if len(state['emails']) == 0:
            custom_log("## No new emails")
            return "end"
        else:
            custom_log("## New emails")
            return "continue"


    @staticmethod
    def extract_sheet_id(url: str) -> Optional[str]:
        """
        Extracts the sheet ID from a Google Sheets URL.

        The sheet ID is the string found between `/d/` and the next `/` or query parameters in the URL.

        Args:
            url (str): The URL of the Google Sheets document.

        Returns:
            Optional[str]: The extracted sheet ID if found, otherwise None.
        """
        pattern = r"/d/([a-zA-Z0-9_-]+)/"
        match = re.search(pattern, url)
        return match.group(1) if match else None