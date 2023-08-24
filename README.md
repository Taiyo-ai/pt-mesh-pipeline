# Data Engineering Task Assignment
## Company: Taiyo.AI

### Task Description
Task is to create a scraper from one of the website from Time Series data or Projects and Tenders, I chose to scrape the data from <strong>E-procurement Government of India: https://etenders.gov.in/eprocure/app </strong> from Projects and Tenders with Python language.


### Required Packages
BeautifulSoup4 \
captcha-solver \
lxml \
pandas \
requests \
selenium \
webdriver-manager \

### Project Description
The <strong>E-procurement Government of India</strong> webiste is the central public procurement portal of <strong>Governamanet of India</strong> for eProcurement. It has various services to get the information about the latest tenders, tenders by location, tenders by organization, tenders status etc. Bidders can enroll also.

In this webscraping project, I am extracting latest tenders data and tenders data by location. \ 
* Used 'Beautiful Soup' for getting latest tenders data and exported the retrieved data to csv file.
* Used 'Selenium' to navigate to <strong>Tenders by Location</strong> page and input the location based on the given location.
* The <strong>Tenders by Location</strong> page also consists of <strong>captcha</strong>, which I cannot able to bypass to automatic extraction, but find a workaround to get the captcha image and entering the data of the captcha with the help of 'captcha-solver' and giving that input to the page via 'selenium'. The resultant data exported to csv file.
* The files exported have date embedded in the filename.

Note: \ 
* Selenium opens chrome web browser while extracting data, so please do not close the browser, which will result in error, the browser closes after the execution of the program.
* Use virtual environment to isolate the environment from the base environment.

### Credits
I Would like to thank <strong>Taiyo.AI<strong> for giving this opportunity to work on the task, which enhanced my knowlegde and credit to <strong>Governament of India</strong> for providing the data in an opne environment.