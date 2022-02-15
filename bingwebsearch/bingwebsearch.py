import json
import os
from datetime import datetime
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from rich import inspect, print


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
    

class Item(BaseModel):
    answer_type: str = Field(alias="answerType")
    result_index: int = Field(alias="resultIndex")
    value: Dict[str, str] = Field(alias="value")
    

class Mainline(BaseModel):
    items: Optional[List[Item]] = Field(None, alias="items")
    

class RankingResponse(BaseModel):
    mainline: Optional[Mainline] = Field(None, alias="mainline")
    


class WebPages(BaseModel):
    web_search_url: Optional[str] = Field(alias="webSearchUrl")
    total_estimated_matches: int = Field(alias="totalEstimatedMatches")
    some_results_removed: Optional[bool] = Field(alias="someResultsRemoved")
    value: List[Value]

    
class SearchResponse(BaseModel):
    """Class to represent the response from the Bing Web Search API.
    
    See the Bing Web Search API for more details:
    https://www.microsoft.com/en-us/bing/apis/bing-web-search-api
    """
    type: str = Field(alias="_type")
    computation: Optional[str] = Field(alias='computation')
    entities: Optional[str] = Field(alias='entities')
    images: Optional[str] = Field(alias='images')
    news: Optional[str] = Field(alias='news')
    query_context: Dict[str, str] = Field(alias="queryContext")
    ranking_response: Optional[RankingResponse] = Field(alias='rankingResponse')
    related_searches: Optional[str] = Field(alias='relatedSearches')
    spell_suggestions: Optional[str] = Field(alias='spellSuggestions')
    time_zone: Optional[str] = Field(alias='timeZone')
    videos: Optional[str] = Field(alias='videos')
    web_pages: Optional[WebPages] = Field(alias='webPages')


def bingwebsearch(
    # Parameters
    q: str,
    answer_count: Optional[int] = None,
    cc: Optional[str] = None,
    count: int = 10,
    freshness: Optional[str] = None,
    mkt: Optional[str] = None,
    offset: Optional[int] = None,
    promote: Optional[str] = None,
    response_filter: Optional[List[str]] = None,
    safe_search: str = "Moderate",
    set_lang: Optional[str] = None,
    text_decorations: Optional[str] = None,
    text_format: Optional[str] = None,
    # Headers
    subscription_key: Optional[str] = None,
    accept_language: Optional[str] = None,
    pragma: Optional[str] = None,
    user_agent: Optional[str] = None,
    # Other
    endpoint: str = "https://api.bing.microsoft.com/v7.0/search",
    save_json: Optional[str] = None
) -> SearchResponse:

    # Check environment variables.
    if subscription_key is None:
        subscription_key = os.getenv('BING_SEARCH_V7_SUBSCRIPTION_KEY')

    # Set up query parameters.
    params_input = {
        "answerCount": answer_count,
        "cc": cc,
        "q": q,
        "count": count,
        "freshness": freshness,
        "mkt": mkt,
        "offset": offset,
        "promote": promote,
        "responseFilter": response_filter,
        "safeSearch": safe_search,
        "setLang": set_lang,
        "textDecorations": text_decorations,
        "textFormat": text_format,
    }
    
    # Delete any dict items where the value is None.
    params = {k: v for k, v in params_input.items() if v is not None}

    # Set up query headers.
    headers_input = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Accept-Language': accept_language,
        'Pragma': pragma,
        'User-Agent': user_agent
    }
    
    # Delete any dict items where the value is None.
    headers = {k: v for k, v in headers_input.items() if v is not None}
    
    # Execute the query
    r = requests.get(endpoint, headers=headers, params=params)
    
    # Save the json file.
    if save_json:
        with open(save_json, "w") as f:
            json.dump(r.json(), f, indent=4)

    # Parse data with Pydantic.
    api_response = SearchResponse(**r.json())

    return api_response

# ==============================================================================
# Testing
# ==============================================================================
load_dotenv()  # take environment variables from .env.

result = bingwebsearch(
    "Wayne Gretzky",
    count=2,
    response_filter=['Webpages'],
    save_json="tmp.json"
)

print(result)
