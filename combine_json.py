import json

def combine_json_files():
    # Read the first JSON file
    with open('google.json', 'r', encoding='utf-8') as f:
        google_urls = set(json.load(f))

    # Read the second JSON file
    with open('news.json', 'r', encoding='utf-8') as f:
        news_urls = set(json.load(f))

    # Combine both sets of URLs (this automatically removes duplicates)
    combined_urls = list(google_urls.union(news_urls))

    # Save the combined results
    with open('combined.json', 'w', encoding='utf-8') as f:
        json.dump(combined_urls, f, indent=4)

if __name__ == "__main__":
    combine_json_files()