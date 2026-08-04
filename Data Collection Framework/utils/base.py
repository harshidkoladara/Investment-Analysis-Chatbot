import logging
import requests
from utils.get_proxy import get_us_free_proxy

# Set up logging configuration
logger = logging.getLogger("DataCollectionFramework.BaseDownloader")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

class BaseDownloader:
    def __init__(self, args = {}):
        self.use_proxy = True if "use_proxy" in args.keys() else False
        if self.use_proxy:
            self.country = args["use_proxy"]
        else:
            self.country = None
        
        self.max_retry = args["max_retry"] if "max_retry" in args.keys() else 1
        self.proxy_pages = args["proxy_pages"] if "proxy_pages" in args.keys() else 5
        
        if self.use_proxy:
            self.proxy_id = 0
            self.proxy_list = self._update_proxy()
        else:
            self.proxy_list = []   
        
    def _get_proxy(self):
        if self.use_proxy:
            if len(self.proxy_list) > 0:
                proxy = self.proxy_list[self.proxy_id]
                self.proxy_id += 1
                if self.proxy_id == len(self.proxy_list):
                    self.proxy_id = 0 
                return proxy
        return None

    def _update_proxy(self):
        try:
            return get_us_free_proxy(self.proxy_pages)
        except Exception as e:
            logger.error(f"Failed to update proxy list: {e}")
            return []

    def _request_get(self, url, headers = None, verify = None, params = None):
        if headers is None:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0"
            }
        max_retry = self.max_retry
        response = None
        for attempt in range(max_retry):
            proxies = self._get_proxy()
            try:
                response = requests.get(url = url, proxies = proxies, headers = headers, verify = verify, params = params, timeout=10)
                if response.status_code == 200:
                    break
                else:
                    logger.warning(f"GET Request to {url} returned status code {response.status_code} (Attempt {attempt+1}/{max_retry})")
            except Exception as e:
                logger.error(f"GET Request to {url} failed: {e} (Attempt {attempt+1}/{max_retry})")
                response = None

        if response is not None and response.status_code != 200:
            response = None

        return response
    
    def _request_post(self, url, headers, json):
        max_retry = self.max_retry
        response = None
        for attempt in range(max_retry):
            proxies = self._get_proxy()
            try:
                response = requests.post(url = url, headers = headers, json = json, proxies = proxies, timeout=10)
                if response.status_code == 200:
                    break
                else:
                    logger.warning(f"POST Request to {url} returned status code {response.status_code} (Attempt {attempt+1}/{max_retry})")
            except Exception as e:
                logger.error(f"POST Request to {url} failed: {e} (Attempt {attempt+1}/{max_retry})")
                response = None

        if response is not None and response.status_code != 200:
            response = None

        return response

