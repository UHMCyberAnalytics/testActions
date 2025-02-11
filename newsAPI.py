import json
import os
from newsapi import NewsApiClient
from datetime import timedelta
import datetime
news_api_key = os.getenv('NEWS_API_KEY')
newsapi = NewsApiClient(api_key=news_api_key)

file_path = "news.json"

if os.path.exists(file_path):
    with open(file_path, "r") as file:
        existing_urls = set(json.load(file))
else:
    existing_urls = set()


def fetch_and_save_news(queries, file_path=file_path):
    all_existing_urls = set()

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                all_existing_urls = set(json.load(file))
            except json.JSONDecodeError:
                print(f"Warning: JSON decoding error in {file_path}. Starting with an empty URL set.")

    for query in queries:
        today = datetime.datetime.now(datetime.timezone.utc)
        last_week = today - timedelta(days=7)

        from_date = last_week.strftime('%Y-%m-%d')
        to_date = today.strftime('%Y-%m-%d')

        try:
            all_articles = newsapi.get_everything(
                q=query,
                language='en',
                sort_by='relevancy',
                from_param=from_date,
                to=to_date,
                page=1
            )

            if all_articles['status'] == 'ok':
                new_urls = {article['url'] for article in all_articles.get('articles', []) if article and 'url' in article}
            else:
                print(f"Error fetching news for '{query}': {all_articles['message']}")
                continue

            initial_count = len(all_existing_urls)
            new_entries = new_urls - all_existing_urls
            added_count = len(new_entries)

            all_existing_urls.update(new_entries)

            print(f"Results for '{query}':")
            print(f"Total URLs before: {initial_count}")
            print(f"New URLs added: {added_count}")
            print(f"Total URLs now: {len(all_existing_urls)}")
            percentage_added = (added_count / len(all_existing_urls) * 100) if len(all_existing_urls) else 0
            print(f"Percentage of new URLs added: {percentage_added:.2f}%")
            print("-" * 20)

        except Exception as e:
            print(f"An error occurred while fetching news for '{query}': {e}")


    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(list(all_existing_urls), file, indent=4)

    print(f"News URLs for all queries saved to {file_path}")


queries = ["Chinese cyber actors", "chinese hackers", "Chinese APT"]
fetch_and_save_news(queries)