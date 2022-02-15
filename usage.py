from bingwebsearch.bingwebsearch import bingwebsearch
from rich import print
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

result = bingwebsearch(
    "Wayne Gretzky", 
    save_json="response.json"
)

print(result)