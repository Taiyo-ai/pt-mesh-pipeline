import pandas as pd


class  Standards:
    
    def __init__(self,dataframe):
        self.dataframe=dataframe
        
    def stadardize_data(self):
        column_name=['doc_id',
 'notice_status',
 'cpv_code',
 'reception_id',
 'country_iso',
 'town_iso',
 'project_name',
 
 'description',
 'postal_code',
 'email',
 'amount',
 'currency',
 'og_notice_no',
 
 'title',
 'notice_publication_number',
 'publication_date',
 'oj_s__issue_number',
 'town_city_of_the_buyer',
 'official_name_of_the_buyer',
 'original_language',
 'country_of_the_buyer',
 'type_of_buyer',
 'eu_institution_agency',
 'document_sent',
 'type_of_contract',
 'type_of_procedure',
 'notice_type',
 'regulation',
 'type_of_bid',
 'award_criteria',
 'common_procurement_vocabulary_(cpv)',
 'place_of_performance_(nuts)',
 'internet_address_(url)',
 'legal_basis',
 'deadline_date',
 
 
 'latitude',
 'longitude',
 

 
 'country_alpha',
 'country_mfn',
 'currency_code',
 'converted_amount_usd']

        Pub= 'publication_date'
        Dead= 'deadline'
        Doc= 'document'
        Auth= 'authority_name' 
    
        extra_columns=[]
  
        for counter in range (1,101):
            key= Doc + '_id_' +str(counter)
            extra_columns.append(key)
            key= Pub + '_' + str(counter)
            extra_columns.append(key)
            key= Dead + '_' + str(counter)
            extra_columns.append(key)
            key= Doc + '_' + str(counter)
            extra_columns.append(key)
            key= Auth + '_' + str(counter) 
            extra_columns.append(key)



        final_column_name= column_name + extra_columns
        empty_dataframe= pd.DataFrame(columns = final_column_name)
        
        for column in self.dataframe:
            empty_dataframe[column]=self.dataframe[column]
            
        
        return empty_dataframe
          
        


