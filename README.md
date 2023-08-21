## Tender Scraper Pipeline
This pipeline scrapes the "Tenders" from https://etenders.gov.in/eprocure/app. It's divided into 4 stages.

## Stage 1 - Scraping
Scrape the Metadata and RawData from the html
```console
cd dummy-data-project/src
python -m client --step 1  # Scrape the metadata
python -m client --step 2  # Scrape the raw data
```

Check the output in `data` directory.

## Stage 2 - Cleaning
Pending

## Stage 3 - Geocoding
Pending

## Stage 4 - Standardization
Pending
