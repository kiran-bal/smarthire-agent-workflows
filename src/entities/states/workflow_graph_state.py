from typing import TypedDict


class WorkflowGraphState(TypedDict):
    """
    State to manage the vashi workflow
    """
    product_website_url: str
    master_csv_path: str
    master_sheet_id: str
    master_sheet_tab_name: str
    recipients: list[str]
    mail_template: str
    web_search_output: dict
    csv_search_output: list[dict]
    quote_final_output: list[dict]
    mail_draft_output: dict
