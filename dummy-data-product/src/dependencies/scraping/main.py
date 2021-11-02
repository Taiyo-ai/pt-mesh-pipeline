import requests
import json
from bs4 import BeautifulSoup
import csv
import requests
from bs4 import BeautifulSoup

# conn1=mysql.connector.connect(user='root',password='####',host='localhost',database='my_db',port=3306)
# myc1=conn1.cursor(buffered=True)
def extract():
    csv_file = open('Data(with Duplications).csv', 'w+')
    writer = csv.writer(csv_file)

    #Colume Names -

    column = ["Title", "Status", "Summary","Notice Type","Approval Number","Executing Agency","Contractor Name","Address","Total Contract Amount (US$)","Contract Amount Financed by ADB (US$)"]
    writer.writerow(column)

    k=0
    j=0
    while k<1236:
        print("")
        try:
            response = requests.get(f"https://www.adb.org/projects/tenders?page={k}").text
            soup1 = BeautifulSoup(response,'html.parser')
            u=soup1.find_all(class_="item")
            i=0
            while i<20:
                try:
                    u3=f"{u[i]}"
                    soup3=BeautifulSoup(u3,'html.parser')

                    item_title=soup3.find(class_="item-title").get_text()

                    item_meta=soup3.find(class_="item-meta").get_text()

                    item_summary=soup3.find(class_="item-summary").get_text()


                    item_details=soup3.find_all("p")

                    print(f"Sr_No -{j+1}")



                    item_title=item_title.replace('"','')
                    item_title=item_title.replace("'","")
                    item_title=f"{item_title}"
                    item_title=" ".join(item_title.split())
                    print(f"Title: {item_title}\n")

                    item_meta=item_meta.replace('"','')
                    item_meta=item_meta.replace("'","")
                    item_meta=f"{item_meta}"
                    item_meta=" ".join(item_meta.split())
                    print(f"Status: {item_meta}\n")

                    item_summary=item_summary.replace('"','')
                    item_summary=item_summary.replace("'","")
                    item_summary=f"{item_summary}"
                    item_summary=" ".join(item_summary.split())
                    print(f"Summary: {item_summary}")

                    notice_type="Null"
                    approval_number="Null"
                    Executing_Agency="Null"
                    Contractor_Name="Null"
                    Address="Null"
                    Total_Contract_Amount="Null"
                    Contract_Amount_Financed_by_ADB="Null"

                    for mm in range(0,7):
                        try:
                            z=item_details[mm].find_all("span") 
                            uk=z[0].text
                            um=z[1].text

                            if uk=='Notice Type:':
                                notice_type=um


                            elif uk=='Approval Number:':
                                approval_number=um


                            elif uk=='Executing Agency:':
                                Executing_Agency=um



                            elif uk=='Contractor Name:':
                                Contractor_Name=um


                            elif uk=='Address:':
                                Address=um


                            elif uk=='Total Contract Amount (US$):':
                                Total_Contract_Amount=um


                            elif uk=='Contract Amount Financed by ADB (US$):':
                                Contract_Amount_Financed_by_ADB=um

                        except:
                            print("\n")
                            break

                    print(f"Notice Type: {notice_type}")
                    print(f"Approval Number: {approval_number}")
                    print(f"Executing Agency: {Executing_Agency}")
                    print(f"Contractor Name: {Contractor_Name}")
                    print(f"Address: {Address}")
                    print(f"Total Contract Amount (US$): {Total_Contract_Amount}")
                    print(f"Contract Amount Financed by ADB (US$): {Contract_Amount_Financed_by_ADB}")


                    i+=1
                    print("=============================================================================\n")

                    data = [item_title, item_meta, item_summary,notice_type,approval_number,Executing_Agency,Contractor_Name,Address,Total_Contract_Amount,Contract_Amount_Financed_by_ADB]
                    writer.writerow(data)


    #                 try:
    #                     sql1=f"INSERT INTO tender(Title,Status,Summary,Notice_type,Approval_number,Executing_Agency,Contractor_names,Address,Total_contract_Amount,Total_amount_adb) VALUES ('{item_title}','{item_meta}','{item_summary}','{notice_type}','{approval_number}','{Executing_Agency}','{Contractor_Name}','{Address}','{Total_Contract_Amount}','{Contract_Amount_Financed_by_ADB}');"

    #                     myc1.execute(sql1)

    #                     conn1.commit()  
    #                 except Exception as e:
    #                     print(e)

                    j+=1

                except Exception as e:
                    print(e)
                    k+=1
                    break
            k+=1
        except Exception as e:
            print(e)
            k+=1
            continue

    print("Pages Finshed")
    csv_file.close()
