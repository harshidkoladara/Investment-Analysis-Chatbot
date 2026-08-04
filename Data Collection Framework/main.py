import os
import argparse
import logging
from dotenv import load_dotenv

# Load local environment parameters
load_dotenv()

# Setup root logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DataCollectionFramework.Main")


def run_rss_news():
    from news_rss.collect_rss import CollectRSSNews
    logger.info("Starting RSS News Feed downloader...")
    url = "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114"
    rss_feed = CollectRSSNews()
    rss_feed.fetch_rss(url=url)
    
    if not rss_feed.dataframe.empty:
        logger.info(f"RSS Download Results Preview (Total {len(rss_feed.dataframe)} items):")
        print(rss_feed.dataframe[["title", "pubDate"]].head())
        rss_feed.dataframe.to_csv("rss_news_data.csv", index=False)
        logger.info("Saved RSS news data to rss_news_data.csv")
    else:
        logger.warning("No items scraped from RSS feed.")


def run_company_news():
    from news.collect_news import CollectNews
    
    token = os.getenv("FINNHUB_API_KEY")
    if not token:
        logger.error("FINNHUB_API_KEY environment variable is not set. Cannot run company news downloader.")
        return

    logger.info("Starting Company News downloader...")
    config = {
        "max_retry": 3,
        "token": token
    }
    
    # Simple query for verification
    news_downloader = CollectNews(config)
    news_downloader.download_date_range_stock("2026-08-01", "2026-08-02", stock="AAPL")
    news_downloader.gather_content()
    
    df = news_downloader.dataframe
    if not df.empty:
        df.to_csv("company_news.csv", index=False)
        logger.info(f"Successfully saved {len(df)} news items to company_news.csv")
    else:
        logger.warning("No company news gathered for selected ticker/range.")


def run_sec_announcements():
    from announcements.collect_announcements import CollectAnnouncements
    logger.info("Starting SEC EDGAR announcements downloader...")
    config = {
        "max_retry": 3
    }
    downloader = CollectAnnouncements(config)
    
    # Fetch narrow date range to prevent getting rate-limited or blocked
    downloader.download_date_range_stock("2026-07-01", "2026-07-05", stock="AAPL")
    df = downloader.dataframe
    if not df.empty:
        df.to_csv("sec_announcements.csv", index=False)
        logger.info(f"Successfully saved {len(df)} filings to sec_announcements.csv")
    else:
        logger.warning("No SEC filings found for selected ticker/range.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Investment Analysis - Data Collection Framework CLI")
    parser.add_argument(
        "--source",
        choices=["rss", "news", "sec"],
        default="rss",
        help="Select data source to run data collection (default: rss)"
    )
    args = parser.parse_args()
    
    if args.source == "rss":
        run_rss_news()
    elif args.source == "news":
        run_company_news()
    elif args.source == "sec":
        run_sec_announcements()