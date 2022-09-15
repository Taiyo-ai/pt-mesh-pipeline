"""
Main file to run and control the execution of the scraper.
"""

import os
import csv
import datetime
import scraper_function
import concurrent.futures
from itertools import repeat

url = "https://www.contractsfinder.service.gov.uk/Search/Results"

headers = [
    "Title",
    "Location of contract",
    "Value of contract",
    "Procurement reference",
    "Published date",
    "Approach to market date",
    "Closing date",
    "Closing time",
    "Contract start date",
    "Contract end date",
    "Contract type",
    "Procedure type",
    "Contract is suitable for SMEs?",
    "Contract is suitable for VCSEs?",
    "Link",
]

if __name__ == "__main__":
    start = datetime.datetime.now()
    url_list = []
    print("Started the scraping.")
    # Using 2233 (number of projects/tenders on the results page.) manually for keep it simple.
    # We can use # result_no = driver.find_element(By.XPATH, '//*[@id="content"]/p/span') to obtain the same result.
    print("Collecting the URLs.")
    for i in range(1, int(2233 / 20)):
        url_list.append(
            f"https://www.contractsfinder.service.gov.uk/Search/Results?&page={i}#dashboard_notices"
        )
    # Adjust the number of pages here as per requirement.
    num_pages = 20
    lst = scraper_function.url_extract(url_list[:num_pages])
    print("Starting the extraction process.")
    # Opening the CSV Writer and passing it to the threads for saving the data to csv file.
    with open("./results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        csvwriter = csv.DictWriter(f, fieldnames=headers)
        csvwriter.writeheader()
        # Using Concurrent.futures to improve the execution speed. (Set max_workers according to the system.)
        # Here I have tested with 20 workers and it worked just fine.
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            proc = list(
                executor.map(scraper_function.data_extract, lst, repeat(csvwriter))
            )

    print(f"Completed scraping in {datetime.datetime.now() - start}.")
