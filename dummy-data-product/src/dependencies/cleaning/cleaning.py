import pandas as pd
import matplotlib.pyplot as plt


def clean_data():

    print("Cleaning...")

    # make sure that this csv location is correct
    df = pd.read_csv("C:\\Users\\LENOVO\\PycharmProjects\\web_scraping\\tender.csv")
    df["Closing Date"] = pd.to_datetime(df["Closing Date"])
    df["Bid Opening Date"] = pd.to_datetime(df["Bid Opening Date"])
    datetime_dim = df[['Closing Date', 'Bid Opening Date']].drop_duplicates().reset_index(drop=True)
    datetime_dim['closing_hour'] = datetime_dim['Closing Date'].dt.hour
    datetime_dim['closing_day'] = datetime_dim['Closing Date'].dt.day
    datetime_dim['closing_month'] = datetime_dim['Closing Date'].dt.month
    datetime_dim['closing_year'] = datetime_dim['Closing Date'].dt.year
    datetime_dim['closing_weekday'] = datetime_dim['Closing Date'].dt.day_name()
    datetime_dim['Opening_hour'] = datetime_dim['Bid Opening Date'].dt.hour
    datetime_dim['Opening_day'] = datetime_dim['Bid Opening Date'].dt.day
    datetime_dim['Opening_month'] = datetime_dim['Bid Opening Date'].dt.month
    datetime_dim['Opening_year'] = datetime_dim['Bid Opening Date'].dt.year
    datetime_dim['Opening_weekday'] = datetime_dim['Bid Opening Date'].dt.day_name()

    plt.figure(figsize=(10, 5))
    plt.subplot(141)
    count = datetime_dim['Opening_weekday'].value_counts()
    count.plot(kind='bar')
    plt.xlabel('Weekday')
    plt.ylabel('Count')
    plt.title('Opening Weekday Count   ')

    plt.subplot(142)
    count = datetime_dim['closing_weekday'].value_counts()
    count.plot(kind='bar')
    plt.xlabel('Weekday')
    plt.ylabel('Count')
    plt.title('Closing Weekday Count')

    plt.subplot(143)
    count = datetime_dim['closing_hour'].value_counts()
    count.plot(kind='bar')
    plt.xlabel('day')
    plt.ylabel('Count')
    plt.title('closing hour')

    plt.subplot(144)
    count = datetime_dim['Opening_hour'].value_counts()
    count.plot(kind='bar')
    plt.xlabel('day')
    plt.ylabel('Count')
    plt.title('opening hour')
    plt.show()

