from dependencies.cleaning.clean_data import clean_data
from dependencies.scraping.web_scrap_data import scrapper

class procurment_manager():
    """
    This class responsible for calling diffrent modules to give final output
    """
    def __init__(self,url,path) -> None:
        self.url=url
        self.storage_path=path
    
    def scrap_data(self):
        sc=scrapper(self.url)
        web_data=sc.fetch_data()
        df=sc.format_data(web_data)
        return df
    
    def clean_data(self,df):
        cd=clean_data(df)
        df_no_dup=cd.remove_duplicate_rows()
        return df_no_dup

    def save_data(self,df,name):
        df.to_csv(path+name,index=False)

if __name__ == "__main__":
    topic_url = 'https://dot.ca.gov/programs/procurement-and-contracts/contracts-out-for-bid'
    path="data/"
    pm=procurment_manager(url=topic_url,path=path)
    df=pm.scrap_data()
    pm.save_data(df,"Contracts Out for Bid_raw.csv")
    cdf=pm.clean_data(df)
    pm.save_data(cdf,"Contracts Out for Bid_clean.csv")