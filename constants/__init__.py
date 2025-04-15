import os


ROOT_DIR = os.getcwd()

CONFIG_DIR = "config"
CONFIG_DIR_PATH = os.path.join(ROOT_DIR, CONFIG_DIR)

TEMPLATES_DIR = "templates"

# Temporary save folder
TEMP_FOLDER = "temp"

# Agents related config
AGENTS_CONFIG_FILENAME = "agents.yaml"
AGENT_TOOLS_FILENAME = "agent_tools.yaml"
AGENT_CATEGORY_FILENAME = "category.yaml"



SUCCESS_MESSAGE = "successfully completed"

# Lang graph and crew ai variables
NODE_AGENTS_KEY = "agents"
CREW_AGENT_KEY = "agent"
CREW_TASKS_KEY = "tasks"
CREW_TOOLS_KEY = "tools"
CREW_AGENT_GOAL_KEY = "goal"
CREW_AGENT_BACKGROUND_KEY = "backstory"
CREW_AGENT_ROLE_KEY = "role"
CREW_TASK_NAME_KEY = "name"
CREW_TASK_DESCRIPTION_KEY = "description"
CREW_TASK_EXP_OUTPUT_KEY = "expected_output"
CREW_TASK_CONTEXT_KEY = "context"
CURR_EXECUTION_NODE_KEY = "curr_execution_node"
PREV_EXECUTION_NODE_KEY = "prev_execution_node"
LAST_NODE_OUTPUT_KEY = "last_node_output"
CURRENT_DATETIME_KEY = "current_datetime"
NODE_HANDLER_MODULE_PATH_KEY = "src.handlers.nodes"
NODE_INPUTS_KEY = "inputs"
NODE_OUTPUT_FIELD_KEY = "output_field"

NODE_MODULE_KEY = "module"
NODE_METHOD_KEY = "method"

# CrewAI tools
CREW_WEB_RAG_SEARCH_TOOL = "web_rag_search_tool"
CREW_CSV_SEARCH_TOOL = "csv_search_tool"
CREW_API_INVOCATION_TOOL = "api_invocation_tool"
CREW_PDF_TEXT_EXTRACTION_TOOL = "pdf_text_extract_tool"
CREW_SEND_GMAIL_TOOL = "gmail_send_tool"
