import re
import pycountry
import os
import uuid
import json
from dateutil.parser import parse
from datetime import datetime
from Tendar_project.src.dependencies.geocoding.geocoder import GeoCoder
import pandas as pd

class Cleaner():

    def __init__(self, soup, url):
        self.soup = soup
        self.url = url

    @staticmethod
    def alpha_3_code(name):
        country_code = pycountry.countries.get(name=fr'{name}')
        return country_code.alpha_3

    @staticmethod
    def return_value(starting_value, content):
        if '<' in starting_value:
            try:
                value_to_return = re.match(fr'{starting_value}[^<]*', content.strip()) \
                .group().replace(starting_value, '').strip()
            except:
                value_to_return = 'Required field not presented in the source'
        else:
            try:
                value_to_return = re.search(fr'(?<={starting_value})[^<]*', content)\
                    .group().strip().strip(':')
            except:
                value_to_return = fr'{starting_value.strip(":")} not defined in the source'.replace('\\', '')

        return value_to_return

    def dump_data_to_csv(self):
        tender_title = self.soup.find('p', class_='text-center detail-title').text.strip()
        released_date = self.soup.find('div', class_='issue-info text-center').text.strip()
        full_content = str(self.soup.find('div', class_='main-info'))
        original_id = self.return_value('Bidding No', full_content)
        project_name = self.return_value('Project Name:', full_content)
        if 'not defined in the source' in str(project_name):
            project_or_tender = 'T'
        else:
            project_or_tender = 'P'
        bidding_price = self.return_value('Price of Bidding Documents', full_content).split('/')[-1].strip()
        description = self.return_value('<div class="main-info>"', full_content)
        region = self.return_value('Place of Implementation', full_content)

        start_date = self.return_value('Beginning of Selling Bidding Documents', full_content)
        end_date = self.return_value('Ending of Selling Bidding Documents', full_content)
        place_of_bid = self.return_value('Place of Bid', full_content)

        place_of_bid_opening = self.return_value('Place of Bid Opening', full_content)
        bidding_agency = self.return_value('Bidding Agency', full_content)
        bid_opening = self.return_value('Deadline for Submitting Bids/Time of Bid Opening \(Beijing Time\)', full_content)

        try:
            bid_opening_date = parse(bid_opening).strftime('%Y-%m-%d')
            today = datetime.today().strftime('%Y-%m-%d')

            if bid_opening_date == today:
                status = 'Bid ongoing'
            elif bid_opening_date < today:
                status = 'Bidding completed'
            else:
                status = 'Bidding yet to start'
        except:
            status = 'Status not available'

        region_coordinates = GeoCoder(region).geo_coder()
        place_of_bid_coordinates = GeoCoder(place_of_bid).geo_coder()
        place_of_bid_opening_coordinates = GeoCoder(place_of_bid_opening).geo_coder()
        """Here we accessing Bidding of china.
         For other countries pass country name to get code"""
        country_code = fr'ISO 3166-1 {self.alpha_3_code("China")}'

        data_dictionary = {
            'aug_id':uuid.uuid4(),
            'original_id':original_id,
            'tender_title':tender_title,
            'released_date':released_date,
            'project_name':project_name,
            'project_or_tender':project_or_tender,
            'bidding_price':bidding_price,
            'description':description,
            'region':region,
            'region_coordinates':region_coordinates,
            'place_of_bid':place_of_bid,
            'place_of_bid_coordinates':place_of_bid_coordinates,
            'place_of_bid_opening':place_of_bid_opening,
            'place_of_bid_opening_coordinates':place_of_bid_opening_coordinates,
            'bid_opening':bid_opening,
            'status':status,
            'country_code':country_code,
            'bidding_start_date':start_date,
            'bidding_end_date':end_date,
            'bidding_agency':bidding_agency
        }
        df = pd.DataFrame([data_dictionary])

        csv_file_name = 'tenders.csv'
        if os.path.isfile(csv_file_name):
            df.to_csv(csv_file_name, index=False, header=False, mode='a')
        else:
            df.to_csv(csv_file_name, index=False)

        print(self.url)
        print(place_of_bid_coordinates)
        print(original_id)
        print(tender_title)
        print(released_date)
        print(project_name)
        print(bidding_price)
        print(description)
        print(region)
        print(region_coordinates)
        print(country_code)
        print(bid_opening)

