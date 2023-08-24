from src.dependencies.scraping.scraper import Scraper
from src.dependencies.cleaning.cleaner import Cleaner
from src.dependencies.geocoding.geocoder import Geocoder
from src.dependencies.standardization.standardizer import Standardizer

class DataPipeline:
    def __init__(self, config):
        self.config = config

    def run(self):
        # Scraper
        scraper = Scraper(self.config)
        raw_data = scraper.run()

        # Cleaner
        cleaner = Cleaner(self.config)
        cleaned_data = cleaner.run(raw_data)

        # Geocoder
        geocoder = Geocoder(self.config)
        geocoded_data = geocoder.run(cleaned_data)

        # Standardizer
        standardizer = Standardizer(self.config)
        standardized_data = standardizer.run(geocoded_data)

        # Save standardized data (example)
        standardized_data_filename = self.config["path_config"]["standardized_data_path"]
        with open(standardized_data_filename, "w") as f:
            # Implement your saving logic here
            pass

        print("Data pipeline completed.")

if __name__ == "__main__":
    # Example configuration dictionary
    config = {
        # class specific configuration
        "webdriver_path": "path_to_webdriver",
        "PROCESSES": 15,

        # path configurations
        "path_config": {
            "meta_data_path": "rel_path",
            "raw_data_path": "rel_path",
            "cleaned_data_path": "rel_path",
            "geocoded_data_path": "rel_path",
            "standardized_data_path": "rel_path",
        }
    }

    pipeline = DataPipeline(config)
    pipeline.run()
