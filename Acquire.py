#!/usr/bin/py
import MySQLdb as mdb
import sys
import thread
import time
import threading


#Session calculator
def Session_Time(threadName,delay):
   count = 0
   while count < 2:
      count += 1
      time.sleep(delay)
      print ("\nYour are in the application for "+str(count)+"mins (Max 2 mins,Then application will exit)")
      if count >= 2:
          thread.interrupt_main()
#End Session 


users_db = mdb.connect("localhost","root","aadhithan","users")
Device_db = mdb.connect("localhost","root","aadhithan","DeviceType")

cursor = users_db.cursor()
cursor1 = Device_db.cursor()

#intialization
name = {}
i=1
count = 1
valid = "false"
DeviceArray={}
DeviceSpecificArray={}
#End of intialization

#get User_list
sql="select name,password from user_list"
cursor.execute(sql)
data = cursor.fetchall()
name = {key:val for key,val in data}
#End of get User_list

#special access list
sql="select name from user_list where special_access is not null"
cursor.execute(sql)
SpeAcc_list = cursor.fetchall()
SpeAcc=[SP[0] for SP in SpeAcc_list]
# End of special access list

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

#Closing DB connections
def CloseDB():
    users_db.close()
    Device_db.close()
#END CloseDB

try:
    th1=threading.Thread(target=Session_Time,args=("Thr-1", 60))
    th1.daemon = True
    th1.start()
    user_name = raw_input("\nPlease Enter the username:")
    for key in name:
	if ( user_name == key ):
    	        passwd=raw_input("\nEnter your password:")
                print(name[key]+" "+passwd)
		if(passwd != name[key]):
	        	print("\nInvalid password.. UnAuthorized Entry prohibited !!!\n")
			sys.exit()
                #Check user has already 2 devices
                sql="select MAC from AllDeviceList where user_name='"+user_name+"'"
                cursor1.execute(sql)
                UDC=cursor1.fetchall()
                UDCL=[UD[0] for UD in UDC]
                if (len(UDCL) >= 2):
                    print("\nYou has occupied max count of device i.e. (" + str(len(UDCL)) + "). Please remove one and try again..")
                    CloseDB()
                    sys.exit()
                #End of User device count

                #Device Type Selection
                print("\nPlease select type of Device you want:\n1.CBR\n2.AXB6\n3.TCXB6\n4.XF3\n5.XB3\n")
                DeviceArray={1:"CBR",2:"AXB6",3:"TCXB6",4:"XF3",5:"XB3"}
                res,device_need=ValidatingChoice(6)
                if( res is -1 ):
                    CloseDB()
                    sys.exit()
                #device type selection ends
                #Device Selection
                sql="select MAC from AllDeviceList where (Devicetype='"+DeviceArray.get(device_need)+"' and user_name is NULL);"
                cursor1.execute(sql)
                DeviceIps_fetch=cursor1.fetchall()
                DeviceIps=[DI[0] for DI in DeviceIps_fetch]
                i=1
                if not DeviceIps:
                    print("\nNo free Device in "+DeviceArray.get(device_need))
                    CloseDB()
                    sys.exit()
                print("\nFree Device in "+DeviceArray.get(device_need)+":\n")
                for DI in DeviceIps:
                    DeviceSpecificArray.update({i:DI})
                    print (str(i) + ")" + DI)
                    i+=1
                res,Choice=ValidatingChoice(i)
                if (res is -1):
                    CloseDB()
                    sys.exit()
                
                count=0
                while(1):
                    TakenFor=raw_input("\nNumber of hours Device needs(Min 1 hr - Max 24 hrs):")
                    count+=1
                    if (count > 3):
                        print("\nYou have exceeds the max attempts,Assigning default 2 hrs..")
                        TakenFor=2
                        break
                    if TakenFor.isdigit() == False:
                        print("\nInvalid Character !!!.attempts remaining "+ str(3-count))
                        continue
                    TakenFor=int(TakenFor)
                    if (((TakenFor > 24) and user_name not in SpeAcc) or (TakenFor == 0)):
                        print("\nYou have Entered more that max hrs or 0,Please enter proper value. .attempts remaining "+ str(3-count))
                        continue
                    break
                
                sql="update AllDeviceList set user_name='"+user_name+"',DeviceOccuppied=NOW(),TakenFor_HRS="+str(TakenFor)+" where MAC='"+DeviceSpecificArray.get(Choice)+"' AND user_name is NULL;"
                cursor1.execute(sql)
                if cursor1.rowcount == 0:
                    print("\nSorry Some one has picked that device just before you. Try Another..\n")
                    sys.exit()
                Device_db.commit()
                print("\nDevice ("+DeviceSpecificArray.get(Choice)+") assigned to your name..Exiting Application...\n")
                #End of Device Selection

                valid = "true"
    if (valid == "false"):
	print("\nInValid UserID ,please contact your admin to register your ID");
        CloseDB()
        sys.exit()

    # disconnect from server
    CloseDB()
except KeyboardInterrupt:
    print("\nExiting Application\n")
    CloseDB()
    sys.exit()
except:
    print("\nExiting Application\n")
    sys.exit()
