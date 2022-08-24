# 1st Assessment of web scrapping

import urllib.request
import pandas as pd
import lxml
import html5lib

url = "https://dot.ca.gov/programs/procurement-and-contracts/contracts-out-for-bid"

with urllib.request.urlopen(url) as i:
    html = i.read()

data = pd.read_html(html)[0]
print(data)

data.to_csv("caltrans.csv", index=False)
