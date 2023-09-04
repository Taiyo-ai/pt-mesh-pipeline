#World Bank Evaluation and Ratings

import requests
import csv
from bs4 import BeautifulSoup 
import os  # Import the os module for handling file paths

class TenderScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    
    def scrape_world_bank(self):
        url = "https://ieg.worldbankgroup.org/data"
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Write code to extract data from the soup object
        # For example:
        tender_data = []
        tenders = soup.find_all("h3", class_="Content Type : Reports title")
        
        # Debugging: Print the number of found tender elements
        print("Number of found tender elements:", len(tenders))
        
        for tender in tenders:
            # Extract relevant details such as title, description, etc.
            title = tender.find("h2").get_text()
            description = tender.find("div").get_text()
            
            # Append data to the tender_data list
            tender_data.append({"Title": title, "Description": description})
        
        return tender_data
    
    # Other scrape methods for other sources here
    
    def save_to_csv(self, data, filename):
        # Define the data folder path
        data_folder = "data"
        
        # Create the data folder if it doesn't exist
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
        
        # Construct the full file path including the data folder
        full_file_path = os.path.join(data_folder, filename)
        
        # Check if the data list is empty
        if data:
            # Use the keys from the first dictionary in the data list
            fieldnames = data[0].keys()
            
            # Write code to save data to a CSV file
            with open(full_file_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
            
            # Display a success message
            print("Operation successful. CSV file saved in the 'data' folder as:", full_file_path)
        else:
            print("No data to save to the CSV file.")

if __name__ == "__main__":
    scraper = TenderScraper()
    
    # Scrape data from the World Bank source
    world_bank_data = scraper.scrape_world_bank()
    
    # Save data to a CSV file
    scraper.save_to_csv(world_bank_data, "world_bank_tenders.csv")