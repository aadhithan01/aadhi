#!/usr/bin/py
import datetime
import MySQLdb as mdb
from collections import defaultdict

db = mdb.connect("localhost","root","aadhithan","users")
db1 = mdb.connect("localhost","root","aadhithan","DeviceType")
cursor1=db1.cursor()

sql = "select MAC,user_name,Devicetype,TakenFor_HRS,DeviceOccuppied from AllDeviceList where user_name is NOT NULL"
cursor1.execute(sql)

output=cursor1.fetchall()
if output:
    for li in output:
     print("\nDEVICE: " + li[0] + "\nuser-name: " + li[1] + "\nDeviceType: " + li[2] + "\nTakenFor: "+str(li[3])+" hrs\nOccuppied Time: "+ str(li[4]) + "\n");

sql = "select MAC,Devicetype from AllDeviceList where user_name is NULL;"
cursor1.execute(sql)

DL=cursor1.fetchall()

DevList={key:value for key,value in DL}
i=1
if DevList:
    print("\n Free IPs :")
    for key in DevList:
        print ("\n"+str(i)+") "+str(DevList.get(key))+" - "+str(key)+"\n")
else:
    print("\nNo free Ips ...\n")

sql="select MAC,user_name,TakenFor_HRS,DeviceOccuppied from AllDeviceList where DeviceOccuppied is not null"
cursor1.execute(sql)
output=cursor1.fetchall()
if output:
    for LI in output:
        oldtime=LI[3]
#        print("oldtime="+str(oldtime))
        new_dt=datetime.datetime.now()
#        print("newtime="+str(new_dt))
#        print("TakenFOR="+str(LI[2]))
        diff=new_dt-oldtime
        days, seconds = diff.days, diff.seconds
        hours = seconds / 3600
#        print("Hours="+str(hours))
        if hours >= LI[2]:
            sql = "update AllDeviceList set user_name=NULL,TakenFor_HRS=NULL,DeviceOccuppied=NULL where MAC='"+LI[0]+"';"
            cursor1.execute(sql)
            db1.commit()

db1.close()
db.close()
