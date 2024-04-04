import time
import random
from datetime import date
from datetime import datetime
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="data_equipments")
mycursor = mydb.cursor(prepared=True)

#Timer
def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1


circuitList = [3, 5, 7, 8, 9, 13] #7

IdealRunRateList = [116.0483, 0, 30.024, 0, 16.65, 0, 198.8, 266.667, 295, 0, 0, 0, 9.6623] #0-12

#circnt = 0

for i in range(6):
    #Circuit
    cir = circuitList[i]


    #Date
    now = datetime.now()
    dt = now.strftime("%Y-%m-%d %H:%M:%S")


    #SHiftId
    if now.hour <= 12 and now.minute == 0:
        Sid = 1
    else:
        Sid = 2

    #Total,Rejected and Good batches Calculation
    #TotalBatches
    #if i == 1:
    #tBatches = -random.randint(int(IdealRunRateList[cir-1] * 0.9), int(IdealRunRateList[cir-1] * 1.1))
    #else:
    tBatches = random.randint(int(IdealRunRateList[cir-1] * 0.9), int(IdealRunRateList[cir-1] * 1.1))
    #27-33
    #ReectedBatches
    rBatches = random.randint(0, int(IdealRunRateList[cir-1]))
    #0-30
    #print(cir, IdealRunRateList[cir-1], int(IdealRunRateList[cir-1] * 0.9), int(IdealRunRateList[cir-1] * 1.1))

    gBatches = tBatches - rBatches
    print(gBatches)
    if ((gBatches / tBatches) >= 0.75):
        efficient = 1
    else:
        efficient = 0


    sql = "INSERT INTO tblstream1(CircuitId, currDateTime, ShiftId, BatchesProduced, BatchesRejected, Efficient) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (cir, dt, Sid, tBatches, rBatches, efficient)

    mycursor.execute(sql, val)
    mydb.commit()

    countdown(8)

    print("Inserted")




