from bs4 import BeautifulSoup
import requests
import os.path
from typing import List
from pprint import pprint
from urllib.parse import urljoin


class Scrapper:
    countryList = {}

    def __init__(self, url: str, allDownload: bool = False, country: List[str] = None):
        """country will be used to download only valid country files
        all is false as no need to directly download all files at once instead selectively download few country files
        url is used to provide url to the object of scrapper
        """
        self.url = url
        self.session = requests.session()
        self.country = country
        self.all = allDownload
        self.resp = None

    def MakeConn(self):
        try:
            content = self.session.get(self.url)
            content.raise_for_status()
            return content
        except Exception as e:
            raise e

    def Soup(self, response, parser: str = "lxml"):
        if response:
            self.resp = BeautifulSoup(response.content, parser)
            return self.resp
        return None

    def makecountrylist(self, tag, downloadClass, download_link_csv, download_button):
        if self.resp is None:
            print("Response from parsing is None. ")
            return
        tmp = self.resp.find_all(tag, class_=downloadClass)
        download_link = self.resp.find_all(tag, class_=download_link_csv)
        links = []
        meta = [i.text.strip() for i in tmp]
        for i in download_link:
            x = i.findNext("a", class_=download_button, href=True)
            links.append(x["href"])
        del meta[0], meta[1], links[0]
        for i, j in zip(meta, links):
            t = i.split()
            Scrapper.countryList[t[0]] = [t[-1], j]
        return Scrapper.countryList

    def GetCountryDownloadPath(self, country):
        absoluteurl, filename = None, None
        try:
            t = Scrapper.countryList[country]
            absoluteurl = urljoin(self.url, t[-1])
            filename = t[-1].split("/")[-1]
            return absoluteurl, filename
        except Exception as e:
            print("Error : ", e)
        return absoluteurl, filename

    def download(self, path):
        if self.all:
            downloadLink, filename = self.GetCountryDownloadPath("Country")
            self.__downloadFile(path, downloadLink, filename)
            return list(filename)
        elif self.country:
            filelist = []
            for i in self.country:
                downloadLink, filename = self.GetCountryDownloadPath(i)
                print(f"Downloading... {i} with filename as : {filename}")
                name = self.__downloadFile(path, downloadLink, filename)
                filelist.append(name)
            return filelist
        else:
            print("Error while downloading the file ")
            return None

    def __downloadFile(self, path, downloadLink, filename):
        if os.path.isfile(os.path.join(path, filename)):
            print(f"{filename} data file already downloaded")

        else:
            with self.session.get(downloadLink) as rb:
                with open(os.path.join(path, filename), "wb") as f:
                    f.write(rb.content)
        return filename


def main():
    obj = Scrapper(
        "https://opentender.eu/all/download", allDownload=False, country=["Malta"]
    )
    resp = obj.CheckConn()
    obj.Soup(resp)
    obj.makecountrylist(
        "div",
        "download-column download-headline",
        "download-column download-csv",
        "download-button",
    )
    pprint(Scrapper.countryList)
    obj.download()
