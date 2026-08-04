import warnings
warnings.filterwarnings("ignore")

import time
import json
import pandas as pd
from tqdm import tqdm
from lxml import etree

from news_rss.base import NewsRSSDownloader


import logging

logger = logging.getLogger("DataCollectionFramework.CollectRSSNews")

class CollectRSSNews(NewsRSSDownloader):
    def __init__(self, args={}):
        super().__init__(args)
        self.dataframe = pd.DataFrame()
        
    def fetch_rss(self, url=None):
        if not url:
            raise ValueError("Please provide a valid URL to fetch RSS feed.")
        
        self.url = url
        logger.info(f"Fetching RSS feed from: {self.url}")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        }
        
        response = self._request_get(url=self.url, headers=headers)
        if response is None or not response.text:
            logger.error("Failed to retrieve or read content from RSS feed URL.")
            self.dataframe = pd.DataFrame()
            return
            
        try:
            # Parse XML content
            parser = etree.XMLParser(recover=True)
            root = etree.fromstring(response.content, parser=parser)
            
            items = root.xpath("//item")
            data_list = []
            
            for item in items:
                title = "".join(item.xpath("./title/text()")).strip()
                link = "".join(item.xpath("./link/text()")).strip()
                pub_date = "".join(item.xpath("./pubDate/text()")).strip()
                description = "".join(item.xpath("./description/text()")).strip()
                
                # Check for category if present
                categories = item.xpath("./category/text()")
                category = ", ".join(categories) if categories else "General"
                
                data_list.append({
                    "title": title,
                    "link": link,
                    "pubDate": pub_date,
                    "description": description,
                    "category": category
                })
                
            self.dataframe = pd.DataFrame(data_list)
            logger.info(f"Successfully processed {len(self.dataframe)} items from RSS feed.")
        except Exception as e:
            logger.error(f"Error parsing XML RSS feed: {e}")
            self.dataframe = pd.DataFrame()