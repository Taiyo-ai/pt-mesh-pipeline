from bs4 import BeautifulSoup
import requests
import pandas as pd
import plotly.express as px

# target link
link = requests.get("https://opentender.eu/start")
webpage = link.text

# Scrapping required data from target link
soup = BeautifulSoup(webpage, 'html.parser')
country = soup.find("ul").find_all(name="li", class_="portal-link")

# getting a list of countries and tender
te = []
for i in country:
    te.append(i.text.strip("\n"))

# creating a nested dictionary with country and tender as key
country_data = {"Country": [],
                "Tender": []
                }
for j in te:
    data = j.split("\n")
    country_data["Country"].append(data[0])

    # Converting Million string to int number
    try:
        if data[1].split(" ")[1] == "Million":
            number = float(data[1].split(" ")[0]) * 1000000
            country_data["Tender"].append(int(number))

    except IndexError:
        country_data["Tender"].append(int(data[1].replace(",", "")))

# Creating a dataframe using dictionary
df = pd.DataFrame(country_data)
pd.options.display.float_format = '{:,.2f}'.format
df.to_csv("data.csv")


# Creating a bar graph

fig = px.bar(x=df.Country, y=df.Tender, color=df.Country, title="Tender Data")
fig.update_xaxes(title="Country")
fig.update_yaxes(title="Tender")
fig.show()


