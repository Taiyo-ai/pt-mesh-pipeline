import pandas as pd
from pandas import set_option
import os
import pycountry

"""before start of standardization of data changing the working directory to /data """


class standardize:
    def __init__(self, pathtodir):
        self.data = None
        self.listOfcsv = []
        self.pathtodir = pathtodir
        self.filetosave = ""
        self.dir = self.pathtodir.split(os.sep)[-1]

    def isdirexist(self):
        return os.path.isdir(self.pathtodir)

    def listcsv(self):
        return os.listdir(self.pathtodir)

    def __fileNameSave(self):
        self.filetosave = self.pathtodir.split(os.sep)[-1] + "-base.csv"
        self.filetosave = os.path.join(self.pathtodir, self.filetosave)
        return os.path.isfile(self.filetosave)

    def allcsv2single(self):
        # first check if merger file exist or not
        if not self.__fileNameSave():
            for i in self.listcsv():
                if "unavailable" not in i:
                    fullpath = os.path.join(self.pathtodir, i)
                    t = pd.read_csv(fullpath, sep=";")
                    t.drop("tender_row_nr", axis="columns", inplace=True)
                    self.listOfcsv.append(t)
            df = pd.concat(self.listOfcsv, axis=0, join="outer")
            df.to_csv(self.filetosave, index=False)
        else:
            print(f"{self.filetosave} already exist in the directory")

    def readMergedcsv(self) -> pd.DataFrame:
        df = pd.read_csv(self.filetosave, index_col="tender_id")
        return df
