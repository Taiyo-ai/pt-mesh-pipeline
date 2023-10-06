from scraper import ETendersScraper

def main():
    scraper = ETendersScraper()

    scraped_data = scraper.scrape_tender_data()

    if scraped_data is not None:

        output_file = "Output_Gov_tenders.csv"
        scraped_data.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")
    else:
        print("Scraping failed.")

if __name__ == '__main__':
    main()