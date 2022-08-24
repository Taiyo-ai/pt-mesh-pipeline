from dependencies.scraping import scraper
from dependencies.cleaning import cleaning
from dependencies.utils import unzipper
from dependencies.standardization import standardizer
import os

""" my scrapper class can work with list of country you specify to download otherwise give the alldownload = true
and it will download the all tender zip file which is 3.9gb to proceed.So that's why I used 'Malta' and 'cyprus'
as example(dry run) (which have the lowest size among all country.
"""
try:
    print(os.getcwd())
    os.mkdir("data")
except FileExistsError:
    print("Data directory already exists")


# 'data' directory to save the downloaded data according to country name
path = os.path.join(os.getcwd() + os.sep + "data")

"""allDownload = true will download the 3.9gb all tender file but if it is false then use list of country to test the working project"""
obj = scraper.Scrapper(
    "https://opentender.eu/all/download",
    allDownload=False,
    country=["Denmark", "Malta"],
)
resp = obj.MakeConn()
obj.Soup(resp)
clist = obj.makecountrylist(
    "div",
    "download-column download-headline",
    "download-column download-csv",
    "download-button",
)
print(clist)  # generating the all countries tenderies in the opentender website
f = obj.download(path)
un = unzipper.unzip(f, path)
un.extract()  # this will extract all the files from the downloaded as in /data/{filename_country}

# working with data files now !!!
p = [os.path.join(path, i.split(".")[0]) for i in f]
for i in p:
    cl = cleaning.standardize(i)
    cl.allcsv2single()
    df = cl.readMergedcsv()
    # try to  improve the handling of path before the standardization applied
    df = standardizer.standard(df, os.path.join(path, i))
