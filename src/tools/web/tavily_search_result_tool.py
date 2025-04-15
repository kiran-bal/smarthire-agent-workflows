from langchain_community.tools.tavily_search import TavilySearchResults

def get_tavily_search_tool():
    tool = TavilySearchResults()
    return tool
