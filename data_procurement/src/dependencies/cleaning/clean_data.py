

class clean_data():
    def __init__(self,df) -> None:
        self.df=df
    
    def remove_duplicate_rows(self):
        return self.df.drop_duplicates()
