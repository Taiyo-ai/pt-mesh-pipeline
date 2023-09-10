import requests
from lxml import html
import csv
import time
# List of URLs for the three task websites
websites = [
    "https://ieg.worldbankgroup.org/data",  # World Bank Evaluation and Ratings
    "https://www.chinabidding.com/en",  # China Procurement Source 1
    "http://www.ggzy.gov.cn/",  # China Procurement Source 2
    "http://en.chinabidding.mofcom.gov.cn/",  # China Procurement Source 3
    "https://www.cpppc.org/en/PPPyd.jhtml",  # China Procurement Source 4
    "https://www.cpppc.org:8082/inforpublic/homepage.html#/searchresult",  # China Procurement Source 5
    "https://etenders.gov.in/eprocure/app",  # E-procurement Government of India
]

# Headers for the HTTP requests
headers={
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
     "If-Modified-Since": "Sun, 10 Sep 2023 08:00:17 GMT",
    "If-None-Match": 'W/"52906-1694332817000"',
}
# Function to scrape and print important information from a website using XPath and headers
def scrape_website_info_xpath_with_headers(url):
    # Send an HTTP GET request with headers
    extracted_data = {}
    try:
        time.sleep(2)
        response = requests.get(url, headers=headers,timeout=30)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page using lxml
            page_content = html.fromstring(response.content)
            print(f"Important Information from {url}:\n")
            # Use XPath to extract titles
            if url == websites[0]:
                title = page_content.xpath("//title/text()")
                print(title)

                content_titles = page_content.xpath("//td//h3//text()")
                for heading in content_titles:
                    print("heading:", heading)

                # Extract and print image source URLs
                images = page_content.xpath("//td//img//@src")
                for image in images:
                    print("image:", image)

                # Extract and print dashboard links
                dashboard_links = page_content.xpath("//td//h4//a//@href")
                for link in dashboard_links:
                    print("dashboard_link:", link)

                # Extract and print subheadings
                subheadings = page_content.xpath("//td//p/text()")
                for subheading in subheadings:
                    print("subheading:", subheading)
                # Extract and print description text

                description = page_content.xpath(
                    "//div[contains(@class,'field-content')]//p//text()"
                )
                for text in description:
                    print("desctiption:", text)

            elif url == websites[1]:  # Specific logic for the second website
                titles = page_content.xpath("//title/text()")
                new_tenders_data = "".join(
                    page_content.xpath(
                        '//ul[contains(@class,"ui-list ui-list-m ui-list-news")]//li[1]//text()'
                    )
                ).strip()
                tender_changes_data = "".join(
                    page_content.xpath(
                        '//ul[contains(@class,"ui-list ui-list-m ui-list-news")]//li[2]//text()'
                    )
                ).strip()
                evaluation_results = "".join(
                    page_content.xpath(
                        '//ul[contains(@class,"ui-list ui-list-m ui-list-news")]//li[3]//text()'
                    )
                ).strip()
                all_data = "\n".join(
                    page_content.xpath(
                        "//div[contains(@class,'ui-list-div')][1]//ul[1]//li//a//text()"
                    )
                ).strip()

                print("Titles:", titles)
                print("New Tenders Data:", new_tenders_data)
                print("Tender Changes Data:", tender_changes_data)
                print("Evaluation Results:", evaluation_results)
                print("All Data:", all_data)

            elif url == websites[2]:
                titles = page_content.xpath("//title/text()")
                print("Title:", titles)

                policies = page_content.xpath(
                    "//div[contains(@class,'lunbo_tw')]//li//a//font//text()"
                )

                for policy in policies:
                    policy_data = policy
                    print("policy_data: ", policy_data)
                    
                transaction_announcement_data = page_content.xpath(
                    "//div[contains(@class,'main_list_on')]//li//a//font//text()"
                )

                for transaction in transaction_announcement_data:
                    transaction_data = transaction
                    print("transction_data: ", transaction_data)

            elif url == websites[3]:
                titles = page_content.xpath("//title/text()")
                new_tenders = page_content.xpath(
                    '//div[contains(@class,"w360 h286 fr")]//ul//a//text()'
                )
                for new_title in new_tenders:
                    print("new_tenders", new_title)

                tender_changes = page_content.xpath(
                    '//div[contains(@class,"w360 h286 fl")]//ul//a//text()'
                )
                for ten_title in tender_changes:
                    print("tender_changes_data", ten_title)

            elif url == websites[6]:
                titles = page_content.xpath("//title/text()")
                tender_tiles = page_content.xpath(
                    '//div[contains(@id,"vmarquee")]//table[contains(@id,"activeTenders")]//tr//a//text()'
                )
                for title in tender_tiles:
                    print("tender_titles", title)
                corrigendum_title = page_content.xpath(
                    "//tr[5]//table[contains(@class,'list_table')]//tr//a//text()"
                )
                for title_c in corrigendum_title:
                    print("corrigendum_title", title_c)
            else:
                titles = page_content.xpath("//title/text()")
                print("Title:", titles)
                h2_tags = page_content.xpath("//h2/text()")
                for h2 in h2_tags:
                    print("H2:", h2)

            print("\n" + "=" * 50 + "\n")  # Add a separator between websites
            return extracted_data
        else:
            print(
                f"Failed to retrieve the web page from {url}. Status code:",
                response.status_code,
            )
    except requests.exceptions.Timeout:
        print(f"Timeout error occurred while accessing {url}. Skipping this URL.")
    return None

# Initialize a list to store all scraped data
all_scraped_data = []
# Loop through each website and scrape important information
for url in websites:
    scraped_data = scrape_website_info_xpath_with_headers(url)
    if scraped_data:
        all_scraped_data.append(scraped_data)
