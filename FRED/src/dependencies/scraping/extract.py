from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
class Extract:
    def extract(self):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get('https://fred.stlouisfed.org/categories/33058')
        links=['https://fred.stlouisfed.org/series/TERMCBAUTO48NS','https://fred.stlouisfed.org/series/RIFLPBCIANM60NM','https://fred.stlouisfed.org/series/TERMAFCNCNSA']
        for i in links:
            driver.get(i)
            driver.find_element(By.ID,"download-button").click() 
            if(i==('https://fred.stlouisfed.org/series/TERMCBAUTO48NS')):
                driver.get('https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=TERMCBAUTO48NS&scale=left&cosd=1972-02-01&coed=2021-08-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=diamond&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2021-11-02&revision_date=2021-11-02&nd=1972-02-01')
            # if (i=='https://fred.stlouisfed.org/series/TERMCBAUTO48NS'):
            #     driver.find_element(By.ID,"download-data-csv").click()
            if(i==('https://fred.stlouisfed.org/series/RIFLPBCIANM60NM')):
                driver.get('https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=RIFLPBCIANM60NM&scale=left&cosd=2006-08-01&coed=2021-08-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=diamond&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2021-11-02&revision_date=2021-11-02&nd=2006-08-01')
            #Cant get data from this
            #It crashes before I get to download
            if(i==('https://fred.stlouisfed.org/series/TERMAFCNCNSA')):
                driver.get('https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=TERMAFCNCNSA&scale=left&cosd=1971-06-01&coed=2011-01-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2011-01-01&line_index=1&transformation=lin&vintage_date=2021-11-02&revision_date=2021-11-02&nd=1971-06-01')

if __name__ == '__main__':
    obj=Extract()
    obj.extract()
