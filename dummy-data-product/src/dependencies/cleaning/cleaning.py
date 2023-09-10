import logging
import sys
import pandas as pd


class CleanData:
    def __int__(self):
        pass

    logging.info("cleaning data")

    def run(self):
        try:

            df = pd.read_csv(f"C:\\Users\\Tnluser\\Desktop\\pt-mesh-pipeline-main\\data\\main_data\\main_data.csv")
        except FileNotFoundError:
            logging.ERROR(f"{FileNotFoundError.__name__}")
            sys.exit(1)

        # drop rows where every cloumn is null
        df.dropna(how='all')

        df.to_csv(f"C:\\Users\\Tnluser\\Desktop\\pt-mesh-pipeline-main\\data\\clean_data\\clean_data.csv")
