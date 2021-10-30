import requests
from bs4 import BeautifulSoup
import re
import dateutil

result = requests.get("https://www.aishub.net/stations")
print(result)

src = result.text
document = BeautifulSoup(src, 'lxml')

table = document.find("table")
print(table)

#For fetching all information from page 1 to 937. 
for page in list(range(1,937)):
  result = requests.get("https://www.aishub.net/stations?page={}".format(page))
  src = result.text
  document = BeautifulSoup(src, 'lxml')
  table = document.find("table")
  rows = table.find_all("tr")  # Note: this works because find_all is resursive by default
  for row in rows[2:-1]:
    cells = row.find_all(["td", "th"])
    cells_text = [cell.get_text(strip=True) for cell in cells]
    (ID, Status, Uptime, Country, Location, Ships, Distinct, Contributor) = cells_text    
    print(f"{ID}, {Status}, {Uptime}, {Country}, {Location}, {Ships} , {Distinct} , {Contributor}")
