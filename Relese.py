#!/usr/bin/py

import MySQLdb as mdb
from collections import defaultdict
import sys

users_db = mdb.connect("localhost","root","aadhithan","users")
Device_db = mdb.connect("localhost","root","aadhithan","DeviceType")

cursor = users_db.cursor()
cursor1 = Device_db.cursor()

user_name = raw_input("\nEnter your user name:")

sql="select name,password from user_list;"
cursor.execute(sql)
valid = "false"
name = {}
DeviceArray={}
data = cursor.fetchall()
name = {key:val for key,val in data}

#Closing DB connections
def CloseDB():
    users_db.close()
    Device_db.close()
#END CloseDB

#validating the selection counts
def ValidatingChoice(i):
    count=0
    while (1):
        device_choice=raw_input("\nSelect Device SNo:")
        count+=1
        DigitCheck=device_choice.isdigit()
        if (count >3 ):
            print("\nInvalid attempts reached..Exiting Application")
            return -1,0
        elif (DigitCheck == False):
            print("\nInvalid character..!!! Select proper Device Type..Attempts remaining "+ str(3-count))
            continue
        device_choice=int(device_choice)
        if (device_choice >= i or device_choice == 0):
            print("\n!!! Select proper Device Type..Attempts remaining "+ str(3-count))
            continue
        break
    return 0,device_choice
#End of validating the selection counts

for key in name:
        if ( user_name == key ):
    		passwd=raw_input("\nEnter your password:")
                if(passwd != name[key]):
                        print("\nInvalid password.. UnAuthorized Entry prohibited !!!\n")
                        CloseDB()
                        sys.exit()
		valid = "true"
                while(1):
                    i=1
                    sql="select MAC,Devicetype from AllDeviceList where user_name='"+user_name+"';"
                    cursor1.execute(sql)
                    DevLisArr = cursor1.fetchall()
                    Device_List={key:val for key,val in DevLisArr}
                    if not Device_List:
                        print("\nNo Device Assigned in your name !!!\n")
                        CloseDB()
                        sys.exit()
                    print("\nDevices in your Name:\n")
                    for DL in Device_List:
                        DeviceArray.update({i:DL})
                        print (str(i) + ")" + DL + "  --  " + Device_List.get(DL))
                        i+=1
                    res,RemDev=ValidatingChoice(i)
                    if( res is -1 ):
                        CloseDB()
                        sys.exit()
                    sql="update AllDeviceList set user_name=NULL,DeviceOccuppied=NULL,TakenFor_HRS=NULL where user_name='"+user_name+"' AND MAC='"+DeviceArray.get(RemDev)+"';"
                    cursor1.execute(sql)
                    Device_db.commit()
                    print("\n"+DeviceArray.get(RemDev)+ " Device removed from your name..")
                    AgainRemove=raw_input("\nWant to remove other devices:YES-Y/NO-press any key:")
                    if (AgainRemove == 'Y' or AgainRemove == 'YES'):
                        continue
                    else:
                        break
                CloseDB()

if (valid == "false"):
	print("\nEnter Valid user id.....!!!!!!!")
        CloseDB()
	sys.exit()

