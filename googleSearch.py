import httpx
import json
import os

api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
search_engine_id = os.getenv("SEARCH_ENGINE_ID")
file_path = "google.json"

if os.path.exists(file_path):
    with open(file_path, "r") as file:
        existing_urls = set(json.load(file))
else:
    existing_urls = set()

queries = ["Chinese cyber actors", "chinese hackers", "Chinese APT"]
def google_search(api_key, search_engine_id, query, **params):
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": search_engine_id,
        "q": query,
        "dateRestrict": "w1",
        **params
    }
    response = httpx.get(base_url, params=params)
    response.raise_for_status()
    return response.json()

def save_search_results(api_key, search_engine_id, query):

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            existing_urls = set(json.load(file))
    else:
        existing_urls = set()
for query in queries:
    search_results = []
    for i in range(1, 100, 10):
        response = google_search(
            api_key=api_key,
            search_engine_id=search_engine_id,
            query=query,
            start=i
        )
        search_results.extend(response.get("items", []))

    new_urls = {item['link'] for item in search_results}

    initial_count = len(existing_urls)
    new_entries = new_urls - existing_urls
    added_count = len(new_entries)

    existing_urls.update(new_entries)

    with open(file_path, "w") as f:
        json.dump(list(existing_urls), f, indent=4)

    total_count = len(existing_urls)
    percentage_added = (added_count / total_count * 100) if total_count else 0

    print(f"Total URLs before: {initial_count}")
    print(f"New URLs added: {added_count}")
    print(f"Total URLs now: {total_count}")
    print(f"Percentage of new URLs added: {percentage_added:.2f}%")

    print(f"Search results saved to {file_path}")