import re
import requests
from tqdm import tqdm
from lxml import etree

def check_us_ips(proxies_list):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}

    can_use = []
    for proxy in tqdm(proxies_list, desc = "Checking ips"):
        try:
            response = requests.get('http://www.google.com', headers=headers, proxies=proxy, timeout=1)
            if response.status_code == 200:
                can_use.append(proxy)
        except Exception as error:
            # print(error)
            pass
    return can_use

def get_us_free_proxy(pages = 10):
    url = "https://openproxy.space/list/http"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Connection Error. Please make sure that your computer now have the access to Google.com")
    
    res = etree.HTML(response.text)
    http_type = "HTTP"
    proxies_list = []

    scripts = res.xpath("//script")
    content = scripts[3].xpath(".//text()")
    pattern = re.compile('LIST",data:(.+),added:')
    result_list = pattern.findall(content[0])
    result_list = result_list[0].strip("[{").strip("}]").split("},{")

    
    for result in result_list:
        pattern = re.compile('\[(.+)\]')
        result = pattern.findall(result)
        result = result[0].split(",")
        result = [r.strip("\"") for r in result]
        for ip in result:
            proxies_list.append(
                {http_type: ip}
            )
    total = pages* 15
    proxies_list = proxies_list[:total] 
    
    can_use = check_us_ips(proxies_list)
    print(f'Get proxy ips: {len(proxies_list)}.')
    print(f'Usable proxy ips: {len(can_use)}.')

    return can_use

