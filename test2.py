
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

# Initialize the Markdown generator
md_generator = DefaultMarkdownGenerator(
    content_filter=PruningContentFilter(threshold=1, threshold_type="dynamic")
)
config = CrawlerRunConfig(
    remove_forms=True,              # Optionally remove form elements
)

# Main async function to crawl
async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://www.itsecurityguru.org/2025/02/04/ai-powered-cyber-warfare-ransomware-evolution-and-cloud-threats-shape-2025-cyber-landscape/", config=config)
        print(result.markdown)

# Run the async main function
import asyncio
asyncio.run(main())
