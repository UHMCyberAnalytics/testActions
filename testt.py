import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter

urls = ["https://www.techdirt.com/2025/02/07/uk-orders-apple-to-break-encryption-worldwide-while-world-is-distracted/",
        "https://www.computerweekly.com/resources/IT-security",
        "https://securityaffairs.com/174005/hacking/playstation-network-global-outage.html",
        "https://www.pbs.org/newshour/politics/patels-roster-of-foreign-clients-draws-scrutiny-over-conflicting-interests-with-the-fbi",
        "https://economictimes.indiatimes.com/news/international/global-trends/white-house-orders-cia-to-send-an-unclassified-email-with-names-of-some-employees/articleshow/117965496.cms",
        "https://www.voanews.com/a/thailand-leader-seeks-more-cooperation-with-china/7968278.html",
        "https://www.cyfirma.com/news/weekly-intelligence-report-07-feb-2025/"]
async def main(urls):


    # Fetch the markdown content for all URLs
    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun_many(
            urls,
        )

    for res in results:
        if res.success:
            print(res.markdown, "crawled OK!")
        else:
            print("Failed:", res.url, "-", res.error_message)

if __name__ == "__main__":
    asyncio.run(main(urls))