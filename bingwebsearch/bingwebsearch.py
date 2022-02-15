from .models import ApiResponse
from typing import List


def bingwebsearch(
    q: str,
    count: int = 10,
    response_filter: List[str] = ['Webpages'],
    mkt: str = 'en-CA',
    subscription_key: str = None,
    endpoint: str = "https://api.bing.microsoft.com/v7.0/search"
) -> ApiResponse:

    # Check environment variables.
    if subscription_key is None:
        subscription_key = os.getenv('BING_SEARCH_V7_SUBSCRIPTION_KEY')

    # Set up query parameters and headers.
    params = {
        "q": q,
        "count": count,
        "responseFilter": response_filter,
        "mkt": mkt
    }

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    
    # Execute the query
    r = requests.get(endpoint, headers=headers, params=params)

    # Parse data with Pydantic.
    api_response = ApiResponse(**r.json())
    api_response._response = r

    return api_response