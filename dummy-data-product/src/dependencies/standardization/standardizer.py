
from datetime import datetime

class StandardizeData:
    
    
    @classmethod
    def standardize_data(cls,data):
        """
        makes the titles snake case
        """
        
        standard_data = {}
        for key,value in data.items():
            split_key = key.split(' ')
            joined_key = "_".join([key.lower() for key in split_key])
            standard_data[joined_key] = value
        return standard_data

    @classmethod
    def format_date(cls, data):
        # 10-Feb-2023 06:00 PM
        # YYYY-MM-DD HH:MM:SS format

        for key, value in data.items():
            if "data" in key:
                cleaned_date = []
                for date in value:
                    # date_string = "10-Feb-2023 06:00 PM"
                    date_format = "%d-%b-%Y %I:%M %p"

                    parsed_date = datetime.strptime(date, date_format)
                    new_date_format = "%Y-%m-%d %H:%M:%S"
                    new_date_string = parsed_date.strftime(new_date_format)
                    cleaned_date.append(new_date_string)
                data[key] = cleaned_date
                
        return data