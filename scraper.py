import csv
import json
import asyncio
import aiohttp
import unicodedata
from bs4 import BeautifulSoup


class Scraper:

    def __init__(self):
        self.url = "https://dot.ca.gov/programs/procurement-and-contracts/contracts-out-for-bid"
    
    async def request(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.text()

    async def post_request(self, event_id, cookies):
        async with aiohttp.ClientSession() as session:
            async with session.post("https://caleprocure.ca.gov/nlx3/psc/psfpd1/SUPPLIER/ERP/c/AUC_MANAGE_BIDS.AUC_RESP_INQ_DTL.GBL?Page=AUC_RESP_INQ_DTL&Action=U&AUC_ID="+str(event_id)+"&AUC_ROUND=1&BIDDER_ID=BID0000001&BIDDER_LOC=1&BIDDER_SETID=STATE&BIDDER_TYPE=B&BUSINESS_UNIT=2660", headers={"content-type":"application/x-www-form-urlencoded; charset=UTF-8"}, data="IF-TargetVerb=GET&IF-TargetContent=%5B%7B%22Lbl%22%3A%22attachmentWrapper%22%2C%22Src%22%3A%22div.InFlightAttachment%3Afirst%22%2C%22Data%22%3A%22null%22%2C%22HWA%22%3A%22.%22%2C%22Children%22%3A%5B%7B%22Lbl%22%3A%22attachmentLink%22%2C%22Src%22%3A%22.%22%2C%22Data%22%3A%22text%3Ahref%22%2C%22Children%22%3A%5B%5D%7D%5D%7D%2C%7B%22Lbl%22%3A%22formAction%22%2C%22Src%22%3A%22form%22%2C%22Data%22%3A%22action%3Aifaction%22%2C%22HWA%22%3A%22.%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22popupMessageContent%22%2C%22Src%22%3A%22span.InFlightPopup%22%2C%22Data%22%3A%22html%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22item3%22%2C%22Src%22%3A%22%23RESP_AUC_H0B_WK_AUC_ID_BUS_UNIT%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22eventName%22%2C%22Src%22%3A%22%23AUC_HDR_ZZ_AUC_NAME%2C%23AUC_HDR_AUC_NAME%22%2C%22Data%22%3A%22text%22%2C%22HWA%22%3A%22.%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22expireDateIframe%22%2C%22Src%22%3A%22div%5Bid%24%3D'AUC_COUNTER_WRK_AUC_COUNTER_HTML'%5D%20iframe%22%2C%22Data%22%3A%22src%3Atime-left-src%22%2C%22HWA%22%3A%22.%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22eventIdLabel%22%2C%22Src%22%3A%22div%5Bid*%3D'divRESP_AUC_H0B_WK_AUC_ID_BUS_UNITlbl'%5D%20%3E%20span%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22eventId%22%2C%22Src%22%3A%22%23RESP_AUC_H0B_WK_AUC_ID_BUS_UNIT%22%2C%22Data%22%3A%22text%22%2C%22HWA%22%3A%22.%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22eventFormatLabel%22%2C%22Src%22%3A%22div%5Bid*%3D'divRESP_AUC_H0B_WK_AUC_FORMAT_BIDBERlbl'%5D%20%3E%20span%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22format1%22%2C%22Src%22%3A%22%23RESP_AUC_H0B_WK_AUC_FORMAT_BIDBER%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22format2%22%2C%22Src%22%3A%22%23AUC_HDR_AUC_TYPE%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22eventStartDateLabel%22%2C%22Src%22%3A%22div%5Bid*%3DdivAUC_HDR_AUC_DTTM_STARTlbl%5D%20%3E%20span%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22eventStartDate%22%2C%22Src%22%3A%22%23AUC_HDR_AUC_DTTM_START%22%2C%22Data%22%3A%22text%22%2C%22HWA%22%3A%22.%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22dept%22%2C%22Src%22%3A%22%23SP_BU_GL_CLSVW_DESCR%2C%23BUS_UNIT_TBL_FS_DESCR%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22eventVersionLabel%22%2C%22Src%22%3A%22div%5Bid*%3DdivAUC_HDR_AUC_VERSIONlbl%5D%20%3E%20span%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22eventVersion%22%2C%22Src%22%3A%22%23AUC_HDR_AUC_VERSION%22%2C%22Data%22%3A%22text%22%2C%22HWA%22%3A%22.%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22eventEndDateLabel%22%2C%22Src%22%3A%22div%5Bid*%3DdivAUC_HDR_AUC_DTTM_FINISHlbl%5D%20%3E%20span%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22eventEndDate%22%2C%22Src%22%3A%22span%5Bid%3D'AUC_HDR_AUC_DTTM_FINISH'%5D%22%2C%22Data%22%3A%22text%22%2C%22HWA%22%3A%22.%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22descriptiondetails%22%2C%22Src%22%3A%22%23AUC_HDR_DESCRLONG%22%2C%22Data%22%3A%22html%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22subscribe%22%2C%22Src%22%3A%22%23ZZ_PO_CSCR_WRK_ZZ_SUBSCRIBE_BTN%22%2C%22Data%22%3A%22id%20name%20disabled%20title%20value%3Atext%22%2C%22HWA%22%3A%22.%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22viewPackage%22%2C%22Src%22%3A%22%23RESP_INQ_DL0_WK_AUC_DOWNLOAD_PB%22%2C%22Data%22%3A%22id%20name%20disabled%20title%22%2C%22HWA%22%3A%22.%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22viewAwardDetails%22%2C%22Src%22%3A%22%23RESP_INQ_DL0_WK_AUC_ANALYZE_PB%22%2C%22Data%22%3A%22id%20name%20disabled%20title%22%2C%22HWA%22%3A%22.%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22postAdButton%22%2C%22Src%22%3A%22%23ZZ_VNDR_AD_WRK_VENDOR_LNK%22%2C%22Data%22%3A%22id%20name%20disabled%22%2C%22HWA%22%3A%22.%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22viewAdButton%22%2C%22Src%22%3A%22%23ZZ_VNDR_AD_WRK_VENDOR_DETAILS_PB%22%2C%22Data%22%3A%22id%20name%20disabled%22%2C%22HWA%22%3A%22.%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22contactName%22%2C%22Src%22%3A%22%23AUC_HDR_NAME1%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22phoneLabel%22%2C%22Src%22%3A%22div%5Bid*%3DdivAUC_HDR_PHONElbl%5D%20%3E%20span%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22phoneText%22%2C%22Src%22%3A%22%5Bid%3D'AUC_HDR_PHONE'%5D%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22emailLabel%22%2C%22Src%22%3A%22div%5Bid*%3DdivAUC_HDR_EMAILIDlbl%5D%20%3E%20span%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22emffffailText%22%2C%22Src%22%3A%22%5Bid%3D'RESP_INQ_DL0_WK_EMAILID%24span'%5D%22%2C%22Data%22%3A%22text%22%2C%22HWP%22%3A%22a%5Bid%3D'RESP_INQ_DL0_WK_EMAILID'%5D%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22emailAnchor%22%2C%22Src%22%3A%22a%5Bid%3D'RESP_INQ_DL0_WK_EMAILID'%5D%22%2C%22Data%22%3A%22id%20name%20text%22%2C%22HWA%22%3A%22.%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22conferenceRow%22%2C%22Src%22%3A%22table%5Bid%5E%3D'ACE_ZZ_BID_CNF_VW%24'%5D%22%2C%22Data%22%3A%22null%22%2C%22HWA%22%3A%22.%22%2C%22Children%22%3A%5B%7B%22Lbl%22%3A%22conferenceLabel%22%2C%22Src%22%3A%22%5Bid*%3D'ZZ_BID_CNF_VW_VALUE_XLATlbl%24'%5D%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22conferenceText%22%2C%22Src%22%3A%22%5Bid%5E%3D'ZZ_BID_CNF_VW_COMMENT1%24'%5D%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22dateLabel%22%2C%22Src%22%3A%22%5Bid%5E%3D'ZZ_BID_CNF_VW_DATE1%24'%5D%22%2C%22Data%22%3A%22null%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22dateText%22%2C%22Src%22%3A%22%5Bid%5E%3D'ZZ_BID_CNF_VW_DATE1%24'%5D%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22timeLabel%22%2C%22Src%22%3A%22%5Bid%5E%3D'ZZ_BID_CNF_VW_DUE_DT_TIME%24'%5D%22%2C%22Data%22%3A%22null%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22timeText%22%2C%22Src%22%3A%22%5Bid%5E%3D'ZZ_BID_CNF_VW_DUE_DT_TIME%24'%5D%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22locationLabel%22%2C%22Src%22%3A%22%5Bid%5E%3D'ZZ_BID_CNF_VW_DESCR254_1%24'%5D%22%2C%22Data%22%3A%22null%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22locationText%22%2C%22Src%22%3A%22%5Bid%5E%3D'ZZ_BID_CNF_VW_DESCR254_1%24'%5D%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22commentsLabel%22%2C%22Src%22%3A%22%5Bid%5E%3D'ZZ_BID_CNF_VW_DESCR254_MIXED%24'%5D%22%2C%22Data%22%3A%22null%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22commentsText%22%2C%22Src%22%3A%22%5Bid%5E%3D'ZZ_BID_CNF_VW_DESCR254_MIXED%24'%5D%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%5D%7D%2C%7B%22Lbl%22%3A%22unspscCodeBody%22%2C%22Src%22%3A%22tr%5Bid%5E%3D'trZZ_UNSPSC_CD_VW2%240_row'%5D%22%2C%22Data%22%3A%22null%22%2C%22Children%22%3A%5B%7B%22Lbl%22%3A%22unspscClassification%22%2C%22Src%22%3A%22%5Bid%5E%3D'ZZ_CATGRY_CD_VW_CATEGORY_CD%24'%5D%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22unspscDescription%22%2C%22Src%22%3A%22%5Bid%5E%3D'ZZ_CAT_DSCR_VW_DESCR254'%5D%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%5D%7D%2C%7B%22Lbl%22%3A%22contractorTblBody%22%2C%22Src%22%3A%22tr%5Bid%5E%3D'trZZ_UNSPSC_CD_VW%240_row'%5D%22%2C%22Data%22%3A%22null%22%2C%22Children%22%3A%5B%7B%22Lbl%22%3A%22contractorTblType%22%2C%22Src%22%3A%22%5Bid%5E%3D'ZZ_LICENS_CD_VW_LICENSE_CODE%24'%5D%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22contractorTblDescription%22%2C%22Src%22%3A%22%5Bid%5E%3D'ZZ_CLS_CD_VW_DESCR254%24'%5D%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%5D%7D%2C%7B%22Lbl%22%3A%22serviceAreaTblBody%22%2C%22Src%22%3A%22tr%5Bid%5E%3D'trZZ_AUC_SA_TBL%240_row'%5D%22%2C%22Data%22%3A%22null%22%2C%22Children%22%3A%5B%7B%22Lbl%22%3A%22serviceAreaID%22%2C%22Src%22%3A%22%5Bid%5E%3D'ZZ_AUC_SA_TBL_ZZ_SRVC_AREA_ID%24'%5D%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22serviceAreaCounty%22%2C%22Src%22%3A%22%5Bid%5E%3D'ZZ_SA_VW_COUNTY%24'%5D%22%2C%22Data%22%3A%22text%22%2C%22Children%22%3A%5B%5D%7D%5D%7D%2C%7B%22Lbl%22%3A%22if_error_items_box%22%2C%22Src%22%3A%22div%5Bid*%3DRESP_ERR_HTMLAREA%5D%3Aeq(0)%22%2C%22HWA%22%3A%22.%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22box_error_items%22%2C%22Src%22%3A%22div%5Bid*%3DRESP_ERR_HTMLAREA%5D%22%2C%22Data%22%3A%22text%22%2C%22HWA%22%3A%22.%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22strCurrScript%22%2C%22Src%22%3A%22script%3Acontains(strCurrUrl)%22%2C%22Data%22%3A%22html%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22windowNum%22%2C%22Src%22%3A%22form%5Bname%5E%3D'win'%5D%22%2C%22Data%22%3A%22name%3Atext%22%2C%22Children%22%3A%5B%5D%7D%2C%7B%22Lbl%22%3A%22hiddenInput%22%2C%22Src%22%3A%22input%5Btype%3Dhidden%5D%22%2C%22Data%22%3A%22id%20name%20value%22%2C%22Children%22%3A%5B%5D%7D%5D&IF-Template=/pages/Events-BS3/event-details.aspx&IF-IgnoreContent=&", cookies=cookies) as resp:
                return await resp.text()

    async def event_ids_extractor(self):
        resp = await self.request(self.url)
        soup = BeautifulSoup(resp, "html.parser")
        table = soup.find_all("table")
        rows = table[0].find_all("tbody")[0].find_all("tr")
        event_ids = []
        for each_row in rows:
            event_ids.append(each_row.find_all("a")[0].text)
        return event_ids

    async def event_ids(self):
        for item in await self.event_ids_extractor():
            yield item

    async def extract_event_data(self, event_id, cookies, output_fh, count):
        resp = await self.post_request(event_id, cookies)
        try:
            data = json.loads(resp)
            clean_event_data = {
                "description": str(data["CaptureResults"]["descriptiondetails"][0]["Properties"]["html"]),
                "sector": str(data["CaptureResults"]["dept"][0]["Properties"]["text"]),
                "timestamp": str({"epublished_date":unicodedata.normalize("NFKD", data["CaptureResults"]["eventStartDate"][0]["Properties"]["text"]),"bid_submission_start_date":unicodedata.normalize("NFKD", data["CaptureResults"]["eventStartDate"][0]["Properties"]["text"]),"bid_submission_end_date":unicodedata.normalize("NFKD", data["CaptureResults"]["eventEndDate"][0]["Properties"]["text"])}),
                "original_id": data["CaptureResults"]["eventId"][0]["Properties"]["text"],
                "name": data["CaptureResults"]["eventName"][0]["Properties"]["text"],
                "county":str(",".join([cnty["Children"]["serviceAreaCounty"][0]["Properties"]["text"] for cnty in data["CaptureResults"]["serviceAreaTblBody"]]))
            }
            event_data = ["",str(count),unicodedata.normalize("NFKD", clean_event_data["original_id"]),"",unicodedata.normalize("NFKD", clean_event_data["name"]),unicodedata.normalize("NFKD", clean_event_data["description"]),"caleprocure","","","","","","",unicodedata.normalize("NFKD", clean_event_data["sector"]),unicodedata.normalize("NFKD", clean_event_data["sector"]),"","","","","","","","","","",unicodedata.normalize("NFKD", clean_event_data["county"]),"","","","",unicodedata.normalize("NFKD", clean_event_data["timestamp"]),""]
            output_fh.writerow(event_data)
        except:
            pass

    tasks = []
    async def create_jobs(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://caleprocure.ca.gov/event/2660/03A3451", allow_redirects=False) as resp:
               cookies = {"InFlightSessionID":resp.cookies["InFlightSessionID"].value}
        count = 0
        output_fh = csv.writer(open("output.csv", "a"))
        output_fh.writerow(["country_code","aug_id","original_id","project_or_tender","name","description","source","status","identified_status","budget","url","document_urls","document_urls","sector","subsector","identified_sector","identified_subsector","identified_sector_subsector_tuple","keywords","entities","country_name","country_code","region_name","region_code","state","county","locality","neighbourhood","location","map_coordinates","timestamps","timestamp_range"])
        async for each_event_id in self.event_ids():
            count += 1
            task = asyncio.ensure_future(self.extract_event_data(each_event_id, cookies, output_fh, count))
            self.tasks.append(task)


scraper = Scraper()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(scraper.create_jobs())
loop.run_until_complete(asyncio.wait(scraper.tasks))