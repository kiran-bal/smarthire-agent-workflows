from crewai_tools import CSVSearchTool

def csv_rag_search_tool(csv_path: str):
    tool = CSVSearchTool(csv=csv_path)
    return tool