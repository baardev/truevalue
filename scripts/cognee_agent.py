#!/usr/bin/env python

import os
import requests
import json

COGNEE_URL = "https://tenant-1f6e75c1-89fc-4caa-bf2a-b5a4e596ac92.aws.cognee.ai"
DATASET = "tv-local-data"

api_key = os.environ.get("COGNEE_API_KEY")
if not api_key:
    raise RuntimeError("Set COGNEE_API_KEY first")

payload = {
    "searchType": "GRAPH_COMPLETION",
    "datasets": [DATASET],
    "query": "What do we know?",
    "topK": 10,
    "onlyContext": False,
    "verbose": True
}

headers = {
    "X-Api-Key": api_key,
    "Content-Type": "application/json"
}

response = requests.post(
    f"{COGNEE_URL}/api/v1/recall",
    headers=headers,
    json=payload,
    timeout=120
)

print("Status:", response.status_code)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))