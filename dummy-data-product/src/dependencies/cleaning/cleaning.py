# dependencies/cleaning/step_3.py
import pandas as pd
import os 

class step_3:
    def __init__(self, config):
        self.config = config

    def run(self):
        # Load your data (assuming it's in a DataFrame)
        data = self.load_data()

        # Perform data cleaning operations
        cleaned_data = self.clean_data(data)

        # Save or use the cleaned data as needed
        self.save_cleaned_data(cleaned_data)

        def save_cleaned_data(self, cleaned_data):
            # Define the data folder
            data_folder = 'data'

            # Create the data folder if it doesn't exist
            if not os.path.exists(data_folder):
                os.makedirs(data_folder)

            # Specify the CSV file name (without the folder name)
            cleaned_data_csv = self.config['cleaned_data_csv']

            # Construct the full file path with the data folder
            csv_file_path = os.path.join(data_folder, cleaned_data_csv)

            # Save the cleaned data to a CSV file within the 'data' folder
            cleaned_data.to_csv(csv_file_path, index=False)
        
    def load_data(self):
        # Load your data here (e.g., from a CSV file or a database)
        data = pd.read_csv(self.config['data_file'])
        return data

    def clean_data(self, data):
        # Treatment of missing fields and values
        data = self.handle_missing_values(data)

        # Conversion of amounts to USD
        data = self.convert_to_usd(data)

        # Treatment of duplicate entries
        data = self.remove_duplicates(data)

        # Convert country codes to ISO 3166-1 alpha3
        data = self.convert_to_alpha3(data)

        # Identify region name and region code using the country code
        data = self.identify_region(data)

        return data

    def handle_missing_values(self, data):
        # Implement logic to handle missing values (e.g., fill with default values)
        data.fillna(value={'column_name': 'default_value'}, inplace=True)
        return data

    def convert_to_usd(self, data):
        # Implement currency conversion logic to USD
        data['amount_usd'] = data['amount'] * self.config['exchange_rate']
        return data

    def remove_duplicates(self, data):
        # Remove duplicate entries based on a set of columns
        data.drop_duplicates(subset=['column1', 'column2'], keep='first', inplace=True)
        return data

    def convert_to_alpha3(self, data):
        # Implement logic to convert country codes to ISO 3166-1 alpha3
        data['country_alpha3'] = data['country_code'].apply(self.get_alpha3_from_code)
        return data

    def get_alpha3_from_code(self, country_code):
        # Implement a function to map country codes to alpha3 codes
        # You can use a mapping dictionary or an external service for this
        return self.config['country_code_mapping'].get(country_code, '')

    def identify_region(self, data):
        # Implement logic to identify region name and code based on country code
        data['region_name'] = data['country_code'].apply(self.get_region_name)
        data['region_code'] = data['country_code'].apply(self.get_region_code)
        return data

    def get_region_name(self, country_code):
        # Implement a function to map country codes to region names
        # You can use a mapping dictionary or an external service for this
        return self.config['region_mapping'].get(country_code, '')

    def get_region_code(self, country_code):
        # Implement a function to map country codes to region codes
        # You can use a mapping dictionary or an external service for this
        return self.config['region_code_mapping'].get(country_code, '')
