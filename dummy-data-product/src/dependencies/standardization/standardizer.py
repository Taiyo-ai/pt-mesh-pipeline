import logging
import datetime
import pandas as pd


class Standardizer:
    def __int__(self):
        pass

    # Standardizing the file
    def run(self):
        try:
            # provide path to csv file
            df = pd.read_csv("<>\\pt-mesh-pipeline-main\\data\\clean_data\\clean_data.csv")
            df.rename(columns={"Unnamed: 0":"id"}, inplace=True)

            # Renaming columns
            for i in df.columns:
                new_col = i.lower()
                new_col = new_col.replace(" ","_")
                df.rename(columns={i:new_col},inplace=True)

            # standardizing date
            for i in df.get("bid_opening_date"):
                i = str(i)
                d = datetime.datetime.strptime(i, "%d-%b-%Y %I:%M %p")
                df.replace(i,d,inplace=True)

            for i in df.get("bid_closing_date"):
                i = str(i)
                d = datetime.datetime.strptime(i, "%d-%b-%Y %I:%M %p")
                df.replace(i, d, inplace=True)

            # save standradized data
            df.to_csv("C:\\Users\\Tnluser\\Desktop\\pt-mesh-pipeline-main\\data\\standardized_data\\standardized_data.csv")

        except pd.errors as error:
            logging.ERROR(f"error accessing file :  {error}")
