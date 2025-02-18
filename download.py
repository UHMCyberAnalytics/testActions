import json
import asyncio
import requests
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.async_dispatcher import SemaphoreDispatcher
import os
import chromadb

client = chromadb.PersistentClient(path=r"C:\Users\Ryder\Documents\GitHub\testActions\something")
GITHUB_URL = "https://raw.githubusercontent.com/UHMCyberAnalytics/testActions/main/combined.json"

def download_json(save_path="combined.json"):
    try:
        response = requests.get(GITHUB_URL)
        response.raise_for_status()
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(response.json(), f)
        print(f"Successfully downloaded and saved {save_path}")
        return True
    except Exception as e:
        print(f"Error downloading JSON: {e}")
        return False

download_json()

# Load the JSON data from the file
with open("combined.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)


# Create or get the collection from Chroma
collection = client.get_or_create_collection(name="my_collection")

# Create the dispatcher for concurrency control
dispatcher = SemaphoreDispatcher(
    max_session_permit=10,  # Maximum concurrent tasks
)

async def main(json_data):
    run_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)

    # Dispatcher to control the number of concurrent tasks for web crawling
    dispatcher2 = SemaphoreDispatcher(
        semaphore_count=5,
    )

    documents = []  # Initialize an empty list for documents
    ids = []  # Initialize an empty list for IDs

    # Fetch the markdown content for all URLs
    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun_many(
            json_data,
            config=run_config,
            dispatcher=dispatcher2
        )

    # Process each result in the list
    for res in results:
        if res.success:
            # Assuming res.markdown contains the crawled document content
            documents.append(res.markdown)
            # Assuming res.urls contain the URL, which you want to use as the ID
            ids.append(res.url)
        else:
            print("Failed:", res.url, "-", res.error_message)

    # Upsert documents into the Chroma collection
    collection.upsert(
        documents=documents,
        ids=ids
    )

def move_to_scraped(json_data):
    scraped_file = "scraped_links.json"
    combined_file = "combined.json"

    # Load existing scraped links
    scraped_urls = set()
    if os.path.exists(scraped_file):
        with open(scraped_file, "r", encoding="utf-8") as file:
            try:
                scraped_urls = set(json.load(file))
            except json.JSONDecodeError:
                scraped_urls = set()

    # Convert json_data to a set and merge
    new_scraped_urls = scraped_urls.union(set(json_data))

    # Save updated scraped links
    with open(scraped_file, "w", encoding="utf-8") as file:
        json.dump(list(new_scraped_urls), file, indent=4)

    # Empty combined.json
    with open(combined_file, "w", encoding="utf-8") as file:
        json.dump([], file, indent=4)

if __name__ == "__main__":
    asyncio.run(main(json_data))
    move_to_scraped(json_data)
