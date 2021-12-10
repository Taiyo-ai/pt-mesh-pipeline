import logging
from datetime import datetime as dt

def clean_budget(amts):
    # amount already in USD
    # convert from string to float
    # add all amounts together
    amt = 0
    for amtText in amts:
        if("million" in amtText):
            amtText = amtText[:amtText.index("million")].strip().replace(",", "")
            amt += float(amtText)*1000000
        else:
            amtText = amtText.strip().replace(",", "")
            amt += float(amtText)
    return amt

def clean_dates(datesUnformated):
    datesFormated = {}
    for key, value in datesUnformated.items():
        # logging.debug(value.strip())
        if(len(value) > (2+1+3+1+4)):
            # logging.debug(value)
            # logging.debug(value[:(2+1+3+1+4)])
            # logging.debug(value[-(2+1+3+1+4):])
            d = dt.strptime(value[:(2+1+3+1+4)], r'%d %b %Y')
            logging.debug(d)
            datesFormated[key.lower().replace(" ", "_")+"_start"] = d.strftime(r'%Y-%m-%d %H:%M:%S')
            d = dt.strptime(value[-(2+1+3+1+4):], r'%d %b %Y')
            logging.debug(d)
            datesFormated[key.lower().replace(" ", "_")+"_end"] = d.strftime(r'%Y-%m-%d %H:%M:%S')
        elif (len(value) < (2+1+3+1+4)):
            pass
        else:
            d = dt.strptime(value, r'%d %b %Y')
            logging.debug(d)
            datesFormated[key.lower().replace(" ", "_")] = d.strftime(r'%Y-%m-%d %H:%M:%S')
    logging.debug(datesUnformated)
    return datesFormated

def sector_subsector_seperation(standardized):
    sec = []
    subsec = []
    for str in standardized:
        sec.append(str[:str.index("/")].strip())
        subsec.append(str[str.index("/")+1:].strip())
    return sec, subsec
    

def sector_subsector_standardisation(rawData):
    standardized = []
    for str in rawData:
        str = str.replace('<p><strong class="sector">', "")
        str = str.replace('</strong>', "")
        str = str.replace('</p>', "")
        str = str.replace('\n', "")
        standardized.append(str)

    return standardized