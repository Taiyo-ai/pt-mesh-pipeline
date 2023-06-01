import requests
import logging
from bs4 import BeautifulSoup

headers = {
    'authority': 'api-endpoint-cons-system.cons-prod-us-central1.kw.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': '',
    'content-type': 'application/json',
    'origin': 'https://kw.com',
    'referer': 'https://kw.com/',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'x-datadog-origin': 'rum',
    'x-datadog-parent-id': '7861482205358451401',
    'x-datadog-sampling-priority': '1',
    'x-datadog-trace-id': '1296716685897060121',
    'x-shared-secret': 'MjFydHQ0dndjM3ZAI0ZHQCQkI0BHIyM='
    }

# Getting HTML page from this function
def get_page(url):
    try:
        res = requests.get(url, headers=headers)
        code = res.status_code
        
        if code == 200:
            page = BeautifulSoup(res.content, "html.parser")
            return page
        else:
            logging.info(f"Request was not successful - Status Code : {code}")
    except Exception as e:
        logging.error(f"Error occured at get_page(): {e}")
    
        