import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import warnings
import logging
import time

warnings.filterwarnings("ignore")

options = Options()
options.add_argument("--ignore-certificate-error")
options.add_argument("--ignore-ssl-errors")
options.add_argument("--headless")
options.add_argument("--incognito")
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

logging.basicConfig(
    filename="./logs.log", format="%(asctime)s %(message)s", filemode="w"
)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def url_extract(url):
    urls = []
    driver = selenium.webdriver.Chrome(
        "./chromedriver_win32/chromedriver.exe", options=options
    )
    for ur in url:
        try:
            driver.get(ur)
            result_no = driver.find_element(By.XPATH, '//*[@id="content"]/p/span')
            link = driver.find_elements(
                By.XPATH, '//./a[@class="govuk-link search-result-rwh break-word"]'
            )
            for i in link:
                urls.append(i.get_attribute("href"))
        except Exception as e:
            logging.error(f"Exception occurred during url_extract: {url, e}", exc_info=True)
    logging.info("Extracted URLs from the web page.")
    return urls


def data_extract(url, writer):
    data = {}
    driver = selenium.webdriver.Chrome(
        "./chromedriver_win32/chromedriver.exe", options=options
    )
    try:
        driver.get(url)
        time.sleep(1)
        try:
            t = driver.find_element(By.XPATH, '//*[@id="all-content-wrapper"]/h1')
            title = t.text.strip() if t else "None"
        except Exception as e:
            logger.exception(f"Skipping url due to H1 tag error.({url})")
            return data
        data["Title"] = title
        p_elems = driver.find_elements(
            By.XPATH, '//*[@id="content-holder-left"]/div[3]/p'
        )
        for i in range(2, len(p_elems) + 1):
            pele = driver.find_element(
                By.XPATH, f'//*[@id="content-holder-left"]/div[3]/p[{i}]'
            )
            hele = driver.find_element(
                By.XPATH, f'//*[@id="content-holder-left"]/div[3]/h4[{i}]'
            )
            data[f"{hele.text}"] = pele.text
        data["Link"] = driver.current_url
        logging.info(f'Scrapped {data["Link"]}')
        driver.close()

        # Call the CSV writer function to save the data to a CSV file ('results.csv').
        data_storage(data, writer)

    except Exception as e:
        logging.error("Exception occurred during data_extract.", exc_info=True)
    return data


def data_storage(entry, writer):
    row = []
    keys = entry.keys()
    try:
        for k in keys:
            row.append(entry[k])
        writer.writerow(
            {
                f'{k}': f'{r}' for k, r in zip(keys, row)
            }
        )
    except Exception as e:
        logger.error(f'Error occurred during saving to CSV. {e}')
