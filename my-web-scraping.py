



import requests
from bs4 import BeautifulSoup
from selenium import webdriver  
import pandas as pd
import numpy as np
import time 
from IPython.display import display
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual,Layout,IntSlider
from tqdm.notebook import tnrange,tqdm


def get_item_num():
    # try:
    r=requests.get('https://www.find-tender.service.gov.uk/Search/Results')
    # print(r.status_code)
    # r=requests.get('https://opentender.eu/')
    html=r.text
    soup=BeautifulSoup(html,"html.parser")
    # print(html)
    # print(soup.find_all('div',{'id':'dashboard_notices'},{'class':'gadget-body'})[0])
    # number_of_items=soup.find('div',{'id':'dashboard_notices'},{'class':'gadget partial-gadget'})
    # number_of_items=number_of_items
    # number_of_items=number_of_items.findChildren('div',{'class':'search-result'})
    number_of_items=soup.find_all('span',{'class':'search-result-count'})[0].get_text().split()[0].replace(',','')
    print(f'The number of records are {int(number_of_items)}')
    print(f'please choose the number of records needed by using the slider')
    return (number_of_items)
    # except: #r.status_code !=200
    #     print(f"wrong response {r.status_code}")
# gets the number of records
num_items=int(get_item_num())
# the widget slider object is initialized
style = {'description_width': 'initial'}
slider=widgets.IntSlider(value=num_items,min=0,max=num_items,step=1,description='Number of Records:',layout=Layout(width='900px'),style=style) 
# display the widget
display(slider)         




# interactive widget having lambda function to return the value from the slider   
choose_records=interactive(lambda num: num,num=slider)
chosen_value=choose_records.children[0].value # capture the value selected by the slider
print(f'{chosen_value} records have been chosen')




def get_url(url):
    """ function to get the response object"""
    #print('in get_url')
    try:
        r=requests.get(url)
        
        #print(f'r code is {r.status_code}')        
        return r
    except:# r.status_code !=200:
        print(f"wrong response {r.status_code}")




output_get_url=get_url('https://www.find-tender.service.gov.uk/Search/Results')
print(f'get_url creates the {type(output_get_url)} object')




def text_url(url):
    """ function to create a html file as backup and extract the html content"""
    #print('in text_url')
    page=get_url(url)
    with open('Results.html', 'a', encoding="utf-8") as file:
        file.write(page.text)        
    text=page.text
       
    #print(f'extract of page :{page.text[:70]}')
    return text




output_text_url=text_url('https://www.find-tender.service.gov.uk/Search/Results')
print(f'text_url creates the {type(output_text_url)} object')




def parse_text(url):
    """function to read in html as beautiful soup object and return the desired table rows"""
    
    page_content=text_url(url)
    #print(f'the length of the webpage is {len(page_content)}')
    soup=BeautifulSoup(page_content,'html.parser')
    soup_div=soup.find_all('div',{'id':"dashboard_notices",'class':'gadget partial-gadget'})
    soup_row=soup_div[0].find_all('div',{'class':'search-result'})
    #print('table extracted')
    return soup_row




output_parse_text=parse_text('https://www.find-tender.service.gov.uk/Search/Results')
print(f'parse_text creates the {type(output_parse_text)} object')




def get_master_list(url):  
    """function to extract table values and append to a dataframe"""
    
    soup_row=parse_text(url)
    master_lst=[] 
    for item in soup_row:        
        for sibling in item.next_siblings:
            if hasattr(sibling,'bs4.element.NavigableString'):
                entry=sibling.find_all('div')
                entry_lst=[]
                for sub_item in entry:
                    entry_lst.append(sub_item.get_text().strip())
                master_lst.append(entry_lst)
    #print('listing done')       
    #print(master_lst[0])
    return master_lst  



output_get_master_list=get_master_list('https://www.find-tender.service.gov.uk/Search/Results')
print(f'get_master_list creates the {type(output_get_master_list)} object')



def main(chosen_value):
    """ main function which cycles through webpages and calls other function"""
    base_url="https://www.find-tender.service.gov.uk/Search/Results?&page="
   
    df_tender=pd.DataFrame()
    len_records=0 
    start_time=time.time()   
    # maximum range cannot exceed the chosen value by the user
    while len_records<=chosen_value:
        for i in tnrange(chosen_value,desc="downloading",total=(chosen_value/1300)): # tnrange will set up the progress bar       
            # slow the querying of url
            time.sleep(0.002)        
            url=base_url+str(i)
            #print(url)
            mlist=get_master_list(url)
            df=pd.DataFrame(mlist)
            df_tender=pd.concat([df_tender,df],ignore_index=True,axis=0)  
            len_records=df_tender.shape[0]   # updation of records obtained
            if len_records>=chosen_value:
                break
    # df_tender.columns=['Country','Start_date','Summary','Deadline']
    # format the date columns for time
    # df_tender['Start_date']=pd.to_datetime(df_tender['Start_date'], format='%d-%b-%Y') # date parsed as datetime
    # df_tender['Deadline']=pd.to_datetime(df_tender['Deadline'], format='%d-%b-%Y')
    current_time=time.time()
    print(f'the time taken is {round(current_time-start_time)} seconds')
    return df_tender
df_main=main(chosen_value)



df_main.to_csv("uk-cabinet.csv",index=None)



