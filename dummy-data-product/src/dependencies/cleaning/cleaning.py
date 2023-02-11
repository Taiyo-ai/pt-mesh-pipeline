class CleanData:
    
    @classmethod
    def clean_data(cls,data):
        
        for key,value in data.items():
            if key == "period_of_work(days)":
                cleaned = [val.strip() for val in value]
                data[key] = cleaned
            
        return data