from os import name
from typing import List
from flask import Flask,render_template,request,url_for,redirect,session
import pyodbc
import datetime
import json



app = Flask(__name__)

con = pyodbc.connect("Driver={SQL Server Native Client 11.0};Server=[DatabaseServerName];database=[DatabaseName];uid=[DatabaseUserName]];pwd=[DatabasePasscode];")
cursor = con.cursor() 

Username = 'Manickavasan K(IN)'



@app.route("/")
def index():
    return render_template('login.html')



@app.route("/DDH_S21/Dashboard")
def dashboard():
    label = "Daily Run DDH S21"
    today_date = datetime.date.today()
    new_today_date = today_date.strftime("%d,%b %Y")
    new_filterdate = today_date.strftime("%Y-%m-%d")
    cursor.execute("select Count(*)Count from [Batch] where CreatedOn > '"+new_filterdate+" 00:00:00' ")
    BarTotal = cursor.fetchone()
    cursor.execute("select * from ( select Count(*)Count from [Batch] where CreatedOn > '"+new_filterdate+" 00:00:00' AND Status = 'JBA S21 SYSTEM ERROR' UNION ALL  select Count(*)Count from [Batch] where CreatedOn > '"+new_filterdate+" 00:00:00' AND Status = 'JBA_COMPLETED' UNION ALL  select Count(*)Count from [Batch] where CreatedOn > '"+new_filterdate+" 00:00:00' AND Status = 'JBA INVALID CREDENTIAL' UNION ALL  select Count(*)Count from [Batch] where CreatedOn > '"+new_filterdate+" 00:00:00' AND Status = 'EMAIL_COMPLETED' UNION ALL  select Count(*)Count from [Batch] where CreatedOn > '"+new_filterdate+" 00:00:00' AND Status = 'JBA S21 NO DATA' UNION ALL  select Count(*)Count from [Batch] where CreatedOn > '"+new_filterdate+" 00:00:00' AND Status = 'OUTQ_FAILED' UNION ALL  select Count(*)Count from [Batch] where CreatedOn > '"+new_filterdate+" 00:00:00' AND Status = 'JBA LOGIN COMPLETED')s")
    BarVlaue = cursor.fetchall()
    values = list()
    i = 0
    for row in BarVlaue:
            values.append(row[i])
    cursor.execute("select Count(*)Count from [Batch] where CreatedOn > '"+new_filterdate+" 00:00:00' AND ProcessType = 'Suppliers'")
    CompletedSupplier = cursor.fetchone()
    cursor.execute("select Count(*)Count from [Batch] where CreatedOn > '"+new_filterdate+" 00:00:00' AND ProcessType = 'Customers'")
    CompletedCustomer = cursor.fetchone()
    cursor.execute("select ScheduleNo,ProcessType,Count(ScheduleNo)Count from [dbo].[CountryMaster] WHERE ISActive = 1 group by ScheduleNo,ProcessType order by ScheduleNo asc")
    Schedules = cursor.fetchall()
    cursor.execute("select Count(*)id from  [dbo].[CountryMaster] WHERE  IsActive = 1 AND ProcessType = 'Customers'")
    CustomerCount = cursor.fetchone()
    cursor.execute("select Count(*)id from  [dbo].[CountryMaster] WHERE  IsActive = 1 AND ProcessType = 'Suppliers'")
    SupplierCount = cursor.fetchone()
    cursor.execute("select Count(CountryCode)Count,CountryCode from  [dbo].[CountryMaster] WHERE ScheduleNo = 99 AND ProcessType = 'Customers' group by CountryCode,ProcessType order by CountryCode asc")
    Customer99 = cursor.fetchall()
    cursor.execute("select Count(CountryCode)Count,CountryCode from  [dbo].[CountryMaster] WHERE ScheduleNo = 99 AND ProcessType = 'Suppliers' group by CountryCode,ProcessType order by CountryCode asc")
    Supplier99 = cursor.fetchall()
    return render_template('index.html',new_today_date = new_today_date,new_filterdate=new_filterdate,Schedules = Schedules,CustomerCount = CustomerCount,
    SupplierCount = SupplierCount,CompletedSupplier=CompletedSupplier,CompletedCustomer=CompletedCustomer,Customer99 = Customer99,Supplier99 = Supplier99,Username = Username,BarTotal=BarTotal,BarVlaue=BarVlaue,values = values)

@app.route("/DDH_S21/Dashboard")
def navigator():
            return render_template('index.html',Username = Username)

@app.route("/DDH_S21")
def S21C():
        cursor.execute("Select DISTINCT BatchNo from [Batch] ORDER BY BatchNo desc")
        BTList = cursor.fetchall()
        return render_template('S21C/table.html',Username = Username,BTList = BTList,TC = '0',sum = 0,EC = '0',NO = '0',ERR = '0',JC = '0',JIC = '0',OUT = '0',ProcessType = 'ProcessType Unavailable')    
        

@app.route("/DDH_S21", methods=["POST","GET"])
def S21Cprocess(): 
        if request.method == 'POST':
              BatchNo = request.form["BatchNo"]
              if BatchNo != '':
                 
                 cursor.execute("select count(*)BatchNo from [Batch] WHERE BatchNo = '"+BatchNo+"' AND Status = 'EMAIL_COMPLETED'")
                 EC = cursor.fetchone()
 
                 cursor.execute("select count(*)BatchNo from [Batch] WHERE BatchNo = '"+BatchNo+"' AND Status = 'JBA S21 NO DATA'")
                 NO = cursor.fetchone()

                 cursor.execute("select count(*)BatchNo from [Batch] WHERE BatchNo = '"+BatchNo+"' AND Status = 'JBA S21 SYSTEM ERROR'")
                 ERR = cursor.fetchone()

                 cursor.execute("select count(*)BatchNo from [Batch] WHERE BatchNo = '"+BatchNo+"' AND Status = 'OUTQ_FAILED'")
                 OUT = cursor.fetchone()
                 cursor.execute("select Country from [Batch] WHERE BatchNo = '"+BatchNo+"' AND Status = 'OUTQ_FAILED'")
                 OUTLIST = cursor.fetchall()

                 cursor.execute("select count(*)BatchNo from [Batch] WHERE BatchNo = '"+BatchNo+"' AND Status = 'JBA_COMPLETED'")
                 JC = cursor.fetchone()

                 cursor.execute("select count(*)BatchNo from [Batch] WHERE BatchNo = '"+BatchNo+"' AND Status = 'JBA INVALID CREDENTIAL'")
                 JIC = cursor.fetchone()

                 cursor.execute("select count(*)BatchNo from [Batch] WHERE BatchNo = '"+BatchNo+"'")
                 TC = cursor.fetchone()

                 cursor.execute("select DISTINCT ProcessType from [Batch] WHERE BatchNo = '"+BatchNo+"'")
                 ProcessType = cursor.fetchone()

                 cursor.execute("select Country from [Batch] WHERE BatchNo = '"+BatchNo+"' AND Status = 'JBA S21 SYSTEM ERROR'")
                 ERRList = cursor.fetchall()

                 cursor.execute("select Country from [Batch] WHERE BatchNo = '"+BatchNo+"' AND Status = 'JBA INVALID CREDENTIAL'")
                 JICList = cursor.fetchall()

                 cursor.execute("select Country from [Batch] WHERE BatchNo = '"+BatchNo+"' AND Status = 'JBA S21 NO DATA'")
                 NoList = cursor.fetchall()
                 

                 cursor.execute("Select DISTINCT BatchNo from [Batch] ORDER BY BatchNo desc")
                 BTList = cursor.fetchall()

                 cursor.execute("SELECT Top(47) * FROM  Batch where BatchNo = '"+BatchNo+"' order by id desc")
                 row = cursor.fetchall()

                 cursor.execute("select Count(*)id from  [dbo].[CountryMaster] WHERE  IsActive = 1 AND ProcessType = '"+ProcessType[0]+"'")
                 CustomerCount = cursor.fetchone()

                 sum = int(TC[0])
                 total = int(CustomerCount[0])
                 sum = sum - total

                 return render_template('S21C/table.html',row = row,TC = TC,EC = EC,NO = NO,ERR = ERR,sum=sum,JC = JC,
                JIC =JIC,BatchNo = BatchNo,BTList = BTList,JICList = JICList,ERRList = ERRList,NoList = NoList,OUTLIST = OUTLIST,OUT = OUT,ProcessType = ProcessType,Username = Username)
              else:
                cursor.execute("Select DISTINCT BatchNo from [Batch] ORDER BY BatchNo desc")
                BTList = cursor.fetchall()
                return render_template('S21C/table.html',TC = '0',EC = '0',NO = '0',sum = 0,ERR = '0',JC = '0',JIC = '0',BTList = BTList,OUT = '0',ProcessType = 'ProcessType Unavailable',Username = Username)
                


        else:
           return render_template('S21C/table.html',TC = '0',EC = '0',NO = '0',ERR = '0',sum = 0,JC = '0',JIC = '0',OUT = '0',ProcessType = 'ProcessType Unavailable',Username = Username)     
    
    
#Debugging the file

if __name__ == "__main__":
    app.run(debug=True)

    
        