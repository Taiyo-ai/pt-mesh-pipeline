import pandas as pd
from pathlib import Path
class Transform:
    def transform2(self):
        df=pd.read_csv(r'C:\Users\Dhyey\Downloads\RIFLPBCIANM60NM.csv')
        # print(df.head())
        df.drop(df[df['RIFLPBCIANM60NM']==('.')].index,inplace=True)
        # print(df.head())
        df=df.reset_index()
        df.drop('index',axis=1,inplace=True)
        df=df.rename(columns={'RIFLPBCIANM60NM': 'Finance rate on consumer installment loans 60 Month Loan'})
        print(df.head())
        filepath = Path('E:/Taiyo/Interest rates for 60 month loan.csv')
        filepath.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filepath)
    def transform1(self):
        df=pd.read_csv(r'C:\Users\Dhyey\Downloads\TERMCBAUTO48NS.csv')
        # print(df.head())
        df.drop(df[df['TERMCBAUTO48NS']==('.')].index,inplace=True)
        # print(df.head())
        df=df.reset_index()
        df.drop('index',axis=1,inplace=True)
        df=df.rename(columns={'TERMCBAUTO48NS': 'Finance rate on consumer installment loans 48 Month Loan'})
        print(df.head())
        filepath = Path('E:/Taiyo/Interest rates for 48 month loan.csv')
        filepath.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filepath)
if __name__ == '__main__':
    obj=Transform()
    obj.transform2()
    obj.transform1()