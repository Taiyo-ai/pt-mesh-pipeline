Project Done By : Paryant Nautiyal

!**! Before Running the client script please go through the following document to understand the project clearly.**

-- **Objective of the Project** 

   - Scrap data for the following sources by getting details of active tenders present on the website
   - URL chosen to scrape => E-procurement Government of India: https://etenders.gov.in/eprocure/app

   - INFO : This project will scrape only active tenders and only 1 page (due to captchas)

   - INFO : you have to manually fill out captchas (or you can add any library) in case you want to scrape more than 1 page. 
   - **WARNING : Using any library/package that automatically solves captchas may result in IP blocking,site not responding(In case it detects it as a bot)**
   
**-- Project** 
   
 

--  Running the script

     # Provide necessary arguments 
        - python -m client.py  --step [1,2,3,4]
     # INFO :  Attempting to run the script without any arguments would result in all possible steps running sequentialy
                  i.e 1 -> 2 -> 3 -> 4
-- Steps should be run in a sequential order i.e 1->2->3->4 , otherwise final data may not be accurate

-- Provide necessary key/values in **.env** file

-- Populate the path variables in utils/paths.py

-- **Logging** 
  - log file Name : newfile.log

-- **Steps** 
   1. Scraped Main Data
   2. Clean Main Data
   3. Geocoded Cleaned Data
   4. Standardized Geocoded Data

-- After Each step file will be saved in data folder 
   - ex main data : /data/main_data/main_data.csv 
