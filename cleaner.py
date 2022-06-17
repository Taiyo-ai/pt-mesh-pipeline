import pandas as pd
import re


def cleaner(cl):
    df = pd.DataFrame()
    dat = []
    tender = []
    Reference_No = []
    OCID = []
    Published_By = []
    Deadline_Date = []
    Notice_Type = []
    for cols in cl:
        dat.append(cols[0])
        col = re.split('\n', cols[1])
        #tender.append(col[0].strip("Opens in new tab"))
        tender.append(re.sub("[\(\[].*?[\)\]]", "", col[0]))
        Reference_No.append(col[2].strip('Reference No:'))
        OCID.append(col[3].strip('OCID:'))
        Published_By.append(col[4].strip('Published By:'))
        Deadline_Date.append(col[5].strip('Deadline Date:'))
        Notice_Type.append(col[6].strip('Notice Type:'))
        
               
    df['Date'] = dat
    df['tender'] = tender
    df['Reference_No'] = Reference_No
    df['OCID'] = OCID
    df['Published_By'] = Published_By
    df['Deadline_Date'] = Deadline_Date
    df['Notice_Type'] = Notice_Type

    return df
