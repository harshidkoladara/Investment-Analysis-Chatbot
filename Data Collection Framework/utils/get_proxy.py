import re
import requests
from tqdm import tqdm
from lxml import etree
import logging

logger = logging.getLogger("DataCollectionFramework.GetProxy")

def check_us_ips(proxies_list):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}
    can_use = []
    for proxy in tqdm(proxies_list, desc="Checking ips"):
        try:
            response = requests.get('http://www.google.com', headers=headers, proxies=proxy, timeout=2)
            if response.status_code == 200:
                can_use.append(proxy)
        except Exception:
            pass
    return can_use

def get_us_free_proxy(pages=10):
    url = "https://openproxy.space/list/http"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        logger.error(f"Failed to fetch proxy list: {e}")
        return []

    if response.status_code != 200:
        logger.error(f"Connection Error: HTTP status {response.status_code}. Cannot access openproxy.space.")
        return []
    
    try:
        res = etree.HTML(response.text)
        http_type = "HTTP"
        proxies_list = []

        scripts = res.xpath("//script")
        if len(scripts) < 4:
            logger.warning("Unexpected page structure: script tags not found.")
            return []
        
        content = scripts[3].xpath(".//text()")
        if not content:
            logger.warning("No inline text found in script tags.")
            return []
            
        pattern = re.compile('LIST",data:(.+),added:')
        result_list = pattern.findall(content[0])
        if not result_list:
            logger.warning("Could not find proxy list data using regular expression.")
            return []
            
        result_list = result_list[0].strip("[{").strip("}]").split("},{")
        
        for result in result_list:
            pattern = re.compile('\[(.+)\]')
            matched = pattern.findall(result)
            if not matched:
                continue
            result = matched[0].split(",")
            result = [r.strip("\"") for r in result]
            for ip in result:
                proxies_list.append({http_type: ip})
        
        total = pages * 15
        proxies_list = proxies_list[:total]
        # Keep checks narrow to speed up operations
        proxies_list = proxies_list[:5]
        can_use = check_us_ips(proxies_list)
        logger.info(f"Retrieved proxy IPs: {len(proxies_list)}.")
        logger.info(f"Usable proxy IPs: {len(can_use)}.")
        return can_use
    except Exception as e:
        logger.error(f"Failed to parse proxy page: {e}")
        return []


