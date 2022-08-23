import requests
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from csv import writer

class Tender:
    def taiyo():
        url= "https://opentender.eu/"
        r= requests.get(url)
        HtmlContent= r.content
        soup= BeautifulSoup(HtmlContent,'html.parser')
        
        
        t1=soup.find("ul").text
        t2=t1.split("\n")
        t3=[]
        
        
        for i in t2:
            if i!='':
                t3.append(i)
        with open ("tender.csv","w",encoding= "utf8", newline='')as f:
            thewriter=writer(f)
            header=["country_name", "no_of_tenders"]
            thewriter.writerow(header)
            type(thewriter)
            x=len(t3)
            for i in range(0,x-1):
                if i%2==0:
                    pair=[t3[i],t3[i+1]]
                    thewriter.writerow(pair)

obj= Tender
obj.taiyo()