
    # Install with pip install firecrawl-py
from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field
from typing import Any, Optional, List

app = FirecrawlApp(api_key='fc-553ee170ae2a4d70bc2131606ff7ffba')

class NestedModel1(BaseModel):
    pool_id: str
    name: str
    liquidity: float
    volume: float

class ExtractSchema(BaseModel):
    pools: list[NestedModel1]

data = app.extract([
  "https://hub.berachain.com/pools/*",
  "https://hub.berachain.com"
], {
    'prompt': 'find all the information related to Bera Chain along with the information in the url link.',
    'schema': ExtractSchema.model_json_schema(),
    'enable_web_search': true
})
    
    
