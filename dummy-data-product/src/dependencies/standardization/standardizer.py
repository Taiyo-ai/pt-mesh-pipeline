


class StandardizeData:
    
    
    @classmethod
    def standardize_data(cls,data):
        """
        makes the titles snake case
        """
        
        standard_data = {}
        for key,value in data.items():
            split_key = key.split(' ')
            joined_key = "_".join([key.lower() for key in split_key])
            standard_data[joined_key] = value
        return standard_data