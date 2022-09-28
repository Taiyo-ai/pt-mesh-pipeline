import sys
import bs4
import requests
import re
import pandas as pd
import pprint
import json

# from ..utils import load_config_yaml
# from ..utils.bucket import (
#     connect_to_buffer_bucket,
#     push_csv_to_buffer_bucket,
# )


class eProcureMetadataScraper:
    def __init__(self):
        self.project_count = 0
        self.header = {
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding':'gzip, deflate, br',
                    'Accept-Language':'en-US,en;q=0.5',
                    'Connection':'keep-alive',
                    'Cookie':'li=https%3A%2F%2Feprocure.gov.in%2Fcppp%2Flatestactivetendersnew; SSESS4e4a4d945e1f90e996acd5fb569779de=9GvnOd8E5i2qRfYE7CLgCoYRdovELv_f08Tdgkd5c7A; cookieWorked=yes',
                    'Host':'eprocure.gov.in',
                    'Referer':'https://eprocure.gov.in/',
                    'Sec-Fetch-Dest':'document',
                    'Sec-Fetch-Mode':'navigate',
                    'Sec-Fetch-Site':'same-origin',
                    'Sec-Fetch-User':'?1',
                    'Upgrade-Insecure-Requests':'1',
                    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0'
                }
        self.page_data = {
                    "tender_reference_number": "",
                    "title": "",
                    "status": "",
                    # Critical Dates
                    "epublished_date": "",
                    "tender_opening_date": "",
                    "bid_opening_date": "",
                    "bid_submission_start_date": "",
                    "bid_submission_closing_date": "",
                    "bid_submission_end_date": "",
                    "document_download_start_date": "",
                    "document_download_end_date": "",
                    # Tender Details
                    "organization_name": "",
                    "organization_type": "",
                    "tender_type": "",
                    "tender_category": "",
                    "product_category": "",
                    "product_sub_category": "",
                    "tender_fee": "",
                    "emd": "",
                    "location": "",
                    "state_name": "",
                    "work_description": "",
                    "corrigendum": "",
                    # Authority Details
                    "inviting_authority_name": "",
                    "inviting_authority_address": "",
                    # URL
                    "tender_document_link": "",
                    "sessioned_url": "",
                }
        # self.config = config
        self.page_url_templates = [
            "https://eprocure.gov.in/cppp/latestactivetendersnew/cpppdata?page={}",
            'https://eprocure.gov.in/cppp/latestactivecorrigendumsnew/cpppdata?page={}',
            'https://eprocure.gov.in/cppp/globaltenders/cpppdata?page={}',
            'https://eprocure.gov.in/cppp/globaltenders/mmpdata?page={}'
            'https://eprocure.gov.in/cppp/highvaluetenders/cpppdata?page={}',
        ]

    def get_project_urls(self):
        i = 0
        reached_last_pages = False
        project_urls = []

        for page_url_template in self.page_url_templates:
            file_name = re.search('e\.gov\.in\/cppp\/([^?]*)', page_url_template).group(1).replace('/', '_')

            # with open(file_name + '_.json', 'w') as json_file:
            #     json_file.write('[')

            while not reached_last_pages:
                print(f"Getting project_ids from page {i + 1}")
                page_url = page_url_template.format(i)
                session = requests.Session()
                response = session.get(page_url, headers=self.header)
                html_data = response.text

                temp_list = self.get_urls_from_page(html_data)

                for t in temp_list:
                    self.parse_url(t, session, file_name)
                i = i + 1

                if temp_list is None:
                    reached_last_pages = True
                    print("All pages scraped")
                else:
                    project_urls.extend(temp_list)
            return project_urls

    def parse_url(self, url, session, file_name):
        while 1:
            try:
                response = session.get(url, headers=self.header)
                soup = bs4.BeautifulSoup(response.text, "lxml")
                try:
                    cid = re.search('https://eprocure.gov.in/cppp/tendersfullview/(.*)', url).group(1)
                    captcha_text = soup.select_one('[data-drupal-selector="edit-captcha-image"]')['alt']
                    captcha_sid = soup.select_one('[name="captcha_sid"]')['value']
                    captcha_token = soup.select_one('[name="captcha_token"]')['value']

                    part_to_add = re.search('https://eprocure.gov.in/cppp/tendersfullview/([^=]*).([^=]*)', url).group(2)
                    # print('Captcha ------ ', captcha_text, captcha_sid, captcha_token)

                    data_payload = {
                        'cid': cid,
                        'captcha_sid': captcha_sid,
                        'captcha_token': captcha_token,
                        'captcha_response':	captcha_text,
                        'op': "Submit",
                        'form_build_id': "form-fClpmN0wqPLHx7STyiqrDJ4vyc1iFFqoNVQfyAInFlk",
                        'form_id': "Tenderfullview_tenders"
                    }
                    session.post(url, data=data_payload, headers=self.header)
                except:
                    session.post(url, headers=self.header)
                    part_to_add = ''

                url_for_response = url+part_to_add
                tender_response = session.get(url_for_response, headers=self.header, verify=False)

                tender_soup = bs4.BeautifulSoup(tender_response.text, "lxml")
                main_table = tender_soup.select('#tfullview [width="100%"]')
                table_text_for_regex = ''
                for t in main_table:
                    clean_table_text = t.text.replace('\n\n\n', ' ').replace(':\n\n', ': ').replace('&amp#x0d', ' ')
                    table_text_for_regex += clean_table_text + '\n'
                # print(table_text_for_regex)

                try:
                    self.page_data['organization_name'] = re.search('Organisation Name\n:(.*)', table_text_for_regex).group(1).strip()
                except:
                    self.page_data['organization_name'] = ''

                try:
                    self.page_data['organization_type'] = re.search('Organisation Type\n:(.*)', table_text_for_regex).group(1).strip()
                except:
                    self.page_data['organization_type'] = ''

                try:
                    self.page_data['title'] = re.search('Tender Title\n:(.*)', table_text_for_regex).group(1).strip()
                except:
                    self.page_data['title'] = ''

                try:
                    self.page_data['tender_reference_number'] = re.search('Tender Reference Number\n:\n(.*)', table_text_for_regex).group(1).strip()
                except:
                    self.page_data['tender_reference_number'] = ''

                try:
                    self.page_data['tender_type'] = re.search('Tender Type\n:\n(.*) Tender', table_text_for_regex).group(1).strip()
                except:
                    self.page_data['tender_type'] = ''

                try:
                    self.page_data['tender_category'] = re.search('Tender Category\n:\n(.*)', table_text_for_regex).group(1).strip()
                except:
                    self.page_data['tender_category'] = ''

                try:
                    self.page_data['product_category'] = re.search('Product Category\n:\n(.*) Product', table_text_for_regex).group(1).strip()
                except:
                    self.page_data['product_category'] = ''

                try:
                    self.page_data['product_sub_category'] = re.search('Product Sub-Category\n:(.*)', table_text_for_regex).group(1).strip()
                except:
                    self.page_data['product_sub_category'] = ''


                if 'Tender Fee' in self.page_data['product_sub_category']:
                    self.page_data['product_sub_category'] = ''

                try:
                    self.page_data['location'] = re.search('Location.*\n:\n(.*)', table_text_for_regex).group(1).strip()
                except:
                    self.page_data['location'] = ''

                try:
                    self.page_data['tender_fee'] = re.search('Tender Fee.*\n:(.*) EMD.*\n:(.*)', table_text_for_regex).group(1).strip()
                except:
                    self.page_data['tender_fee'] = ''

                try:
                    self.page_data['emd'] = re.search('Tender Fee.*\n:(.*) EMD.*\n:(.*)', table_text_for_regex).group(2).strip()
                except:
                    self.page_data['emd'] = ''

                try:
                    self.page_data['epublished_date'] = re.search('ePublished Date\n:(.*)', table_text_for_regex).group(1).strip()
                except:
                    self.page_data['epublished_date'] = ''

                try:
                    self.page_data['bid_opening_date'] = re.search('Bid Opening Date\n:(.*) Doc', table_text_for_regex).group(1).strip()
                except:
                    self.page_data['bid_opening_date'] = ''

                try:
                    self.page_data['document_download_start_date'] = re.search('Document Download Start Date\n:(.*)', table_text_for_regex).group(1).strip()
                except:
                    self.page_data['document_download_start_date'] = ''

                try:
                    self.page_data['document_download_end_date'] = re.search('Document Download End Date\n:(.*) Bid', table_text_for_regex).group(1).strip()
                except:
                    self.page_data['document_download_end_date'] = ''

                try:
                    self.page_data['bid_submission_start_date'] = re.search('Bid Submission Start Date\n:(.*)', table_text_for_regex).group(1).strip()
                except:
                    self.page_data['bid_submission_start_date'] = ''

                try:
                    self.page_data['bid_submission_end_date'] = re.search('Bid Submission End Date\n:(.*)', table_text_for_regex).group(1).strip()
                except:
                    self.page_data['bid_submission_end_date'] = ''

                try:
                    self.page_data['work_description'] = re.search('Work Description\n:(.*)', table_text_for_regex).group(1).strip()
                except:
                    self.page_data['work_description'] = ''

                try:
                    self.page_data['tender_document_link'] = re.search('Tender Document\n:(.*)', table_text_for_regex).group(1).strip()
                except:
                    self.page_data['tender_document_link'] = ''

                try:
                    self.page_data['inviting_authority_name'] = re.search('\n Name\n:(.*)', table_text_for_regex).group(1).strip()
                except:
                    self.page_data['inviting_authority_name'] = ''

                try:
                    self.page_data['inviting_authority_address'] = re.search('Address\n:(.*)', table_text_for_regex).group(1).strip()
                except:
                    self.page_data['inviting_authority_address'] = ''

                self.page_data['sessioned_url'] = url

                pprint.pprint(self.page_data)
                # with open(file_name + '_.json' , 'a') as json_file:
                #     json.dump(self.page_data,json_file,indent=4)
                # with open(file_name + '_.json' , 'a') as f:
                #     f.write(',')
                break
            except:
                print('Try again')
                continue


    @staticmethod
    def get_urls_from_page(html_data):
        projects_urls = []
        soup = bs4.BeautifulSoup(html_data, "lxml")
        links = soup.select("#table a")
        if len(links) == 0:
            return None
        else:
            for url in links:
                project_url = url['href']
                print(project_url)
                projects_urls.append(project_url)
        return projects_urls

    def run(self):
        # try:
            project_urls = self.get_project_urls()
            self.get_urls_df = pd.DataFrame(
                list(project_urls), columns=["url"]
            )
        # except Exception as e:
        #     print(
        #         f"Error occurred. Closing PPPINDIA Metadata scraping process.\n{str(e)}"
        #     )
        # finally:
            # self.bucket = connect_to_buffer_bucket()
            # push_csv_to_buffer_bucket(
            #     self.bucket,
            #     self.project_ids_urls_df,
            #     self.config["reference_urls_path"],
            # )
            # self.get_urls_df.to_csv(
            #     "eprocure_metadata.csv", index=False, header=True
            # )
            #
            # sys.exit()


if __name__ == "__main__":
    # config = load_config_yaml()["paths"][""]
    # PPPINDIAMetadataScraper(config).run()
    e = eProcureMetadataScraper()
    e.run()


