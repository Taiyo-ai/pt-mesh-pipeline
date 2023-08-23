E-Procurement-Portal-Scraper
This is a web-scraper built using Python Selenium Library and collects data of various tenders issued by the Organizations under Government of India

How to use
In the 'src' directory, there is a file named config.json with the following properties:

headless - If 'true' the selenium browser will open in headless mode otherwise it will open in non-headless mode. (recommended value: true)

inprivate - If 'true' the selenium browser will open in 'inprivate' (Incognito) mode to prevent saving of cookies by the website. If 'false' the browser will open in normal mode. (recommended value: true)

output_csv - This is the name of the output data file which will be saved in the 'data' directory. You can change it according to your wish. Make sure to end the name of the file with '.csv'

start_ind - This is the start index from which the scraper will start scraping data from.

end_ind - This is the end index till which the scraper will scrape the data.

NOTE:

Each index represents an organization. to see the total number of organizations, visit: https://etenders.gov.in/eprocure/app?page=FrontEndTendersByOrganisation&service=page
The end index is not included while scraping.
To scrape data from all organizations give a value 0 to start_ind and any number greater than the number of organizations (like 100) to end_ind.
Libraries Used
Selenium: to build web-scraper
Pandas: to read the data
NumPy: to wrangle the data
Note:

All the libraries used are mentioned in the 'requirements.txt' file
This scraper uses Microsoft Edge (Chromium) browser
