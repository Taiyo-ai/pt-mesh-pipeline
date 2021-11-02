import schedule 
import time
from extract import Extract
from trannsform import Transform
def scheduler():
    extr_obj=Extract()
    trans_obj=Transform()
    if __name__ == '__main__':
        schedule.every().day.at("00:00").do(extr_obj.extract())
        schedule.every().day.at("00:00").do(trans_obj.transform1())
        schedule.every().day.at("00:00").do(trans_obj.transform2())

