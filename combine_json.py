import json
import os

def combine_json_files():
    # Read existing URLs from combined.json (if it exists)
    if os.path.exists('combined.json'):
        with open('combined.json', 'r', encoding='utf-8') as f:
            try:
                combined_urls = set(json.load(f))
            except json.JSONDecodeError:
                combined_urls = set()  # Handle empty or invalid JSON
    else:
        combined_urls = set()

    # Read existing URLs from scraped_links.json (if it exists)
    scraped_urls = set()
    if os.path.exists('scraped_links.json'):
        with open('scraped_links.json', 'r', encoding='utf-8') as f:
            try:
                scraped_urls = set(json.load(f))
            except json.JSONDecodeError:
                scraped_urls = set()

    # Read the first JSON file
    with open('google.json', 'r', encoding='utf-8') as f:
        google_urls = set(json.load(f))

    # Read the second JSON file
    with open('news.json', 'r', encoding='utf-8') as f:
        news_urls = set(json.load(f))

    # Combine new URLs while avoiding duplicates from scraped_links.json
    new_urls = (google_urls | news_urls) - scraped_urls

    # Merge with existing combined URLs
    combined_urls.update(new_urls)

    # Save the updated combined results
    with open('combined.json', 'w', encoding='utf-8') as f:
        json.dump(list(combined_urls), f, indent=4)

if __name__ == "__main__":
    combine_json_files()
