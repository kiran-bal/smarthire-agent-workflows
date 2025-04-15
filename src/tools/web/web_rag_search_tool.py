from crewai_tools import WebsiteSearchTool

def web_rag_search_tool(url: str):
    tool = WebsiteSearchTool(website="https://en.wikipedia.org/wiki/Climate_change")
    return tool