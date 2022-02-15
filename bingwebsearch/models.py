from pydantic import BaseModel, Field
from typing import List, Dict


class Value(BaseModel):
    id: str
    name: str
    url: str
    is_family_friendly: bool = Field(alias="isFamilyFriendly")
    display_url: str = Field(alias="displayUrl")
    snippet: str
    date_last_crawled: datetime = Field(alias="dateLastCrawled")
    language: str
    is_navigational: bool = Field(alias="isNavigational")


class WebPages(BaseModel):
    web_search_url: Optional[str] = Field(alias="webSearchUrl")
    total_estimated_matches: int = Field(alias="totalEstimatedMatches")
    some_results_removed: Optional[bool] = Field(alias="someResultsRemoved")
    value: List[Value]

    
class ApiResponse(BaseModel):
    """Class to represent the response from the Bing Web Search API.
    
    See the Bing Web Search API for more details:
    https://www.microsoft.com/en-us/bing/apis/bing-web-search-api
    """
    _response: Optional[str] = None
    _type: str
    query_context: Dict[str, str] = Field(alias="queryContext")
    web_pages: WebPages = Field(alias="webPages")

