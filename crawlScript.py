import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://www.techdirt.com/2025/02/06/but-her-emails-redux-team-trump-makes-cia-send-list-of-all-recently-hired-employees-over-unclassified-email",
        )
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())