from Scraper import Scraper
from get_result import get_result

urls = ['https://etenders.gov.in/eprocure/app',
        'https://www.cpppc.org/en/PPPyd.jhtml',
        'http://www.ggzy.gov.cn/']

if __name__ == '__main__':

    results = []
    results.append([get_result(url) for url in urls])
    print(results)