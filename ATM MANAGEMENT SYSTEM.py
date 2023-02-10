import mysql.connector

mydb= mysql.connector.connect(

    host="localhost",
    user="root",
    password="Muhasina@97"

)

mycursor=mydb.cursor()
sql=('create database if not exists atm')
mycursor.execute(sql)
mycursor.execute('use atm')
mycursor.execute('create table if not exists CUSTOMER(CID int primary key not null,CNAME varchar(200) not null,ADDRESS varchar(200) not null,PHONE int not null)')
mycursor.execute('create table if not exists ACCOUNT(ifsc int primary key not null,AC_NO varchar(200) not null,AC_TYPE varchar(200) not null,PASSWORD varchar(200) not null,Balance int not null,BRANCH varchar(200) not null)')


##Create new customer
def newCustomer():
    print("Please enter the bellow details carefully !!")
    CID=int(input("Enter customer id:"))
    CNAME=input('Enter customer name:')
    ADDRESS=input("Enter customer address:")
    PHONE=int(input('Enter your number:'))
    sql='insert into customer(CID,CNAME,ADDRESS,PHONE) values (%s,%s,%s,%s)'
    values=(CID,CNAME,ADDRESS,PHONE)
    mycursor=mydb.cursor()
    mycursor.execute(sql,values)
    mydb.commit()
    print('***Data entered Successfully***')
    newAccount()

def newAccount():
    print("Create new account")
    ifsc= int(input("Enter ifsc:"))
    AC_NO = input('Enter customer AC_NO:')
    AC_TYPE = input("Enter customer AC_TYPE:")
    PASSWORD= input('Enter your PASSWORD[Use number]:')
    Balance=0
    BRANCH = input("Enter branch details:")
    sql='insert into account(ifsc,AC_NO,AC_TYPE,PASSWORD,Balance,BRANCH) values(%s,%s,%s,%s,%s,%s)'
    values=(ifsc,AC_NO,AC_TYPE,PASSWORD,Balance,BRANCH)
    mycursor=mydb.cursor()
    mycursor.execute(sql,values)
    mydb.commit()
    print('***Account created Successfully***')
    main()

def searchAccount():
    AC_NO=input('Enter customer AC_NO:')
    PASSWORD = input('Enter your PASSWORD:')
    mycursor = mydb.cursor()
    mycursor.execute("select*from account where AC_NO=%s and PASSWORD=%s;",(AC_NO,PASSWORD))
    data=mycursor.fetchone()
    if data:
        print("YOUR ACCOUNT DETAILS")
        print(data)
    else:
        print("***Sorry! Something went wrong,Please try Again***")
    main()
def depositAmount():
    count=3
    IFSC=input("Enter the IFSC code:")
    AC_NO=int(input('Enter your AC_NO:'))

    mycursor.execute("select*from account where AC_NO=%s and IFSC=%s;",(AC_NO,IFSC))
    data=mycursor.fetchall()
    if data:
        while True:
            password = input('Enter your PASSWORD:')
            mycursor.execute("select*from account where PASSWORD=%s;",(password,))
            data=mycursor.fetchall()
            if data:
                amount=int(input("Please enter the amount to deposit:"))
                mycursor.execute("update account set Balance=Balance+(%s);", (amount,))
                mydb.commit()
                mycursor.execute("select Balance from account where ac_no=%s",(AC_NO,))
                myresult=mycursor.fetchone()
                for y in myresult:
                    print("Balance=",y)
                print("***Transaction completed Successfully***")
                break
            else:
                print("***Wrong pin!!,Please try Again ***")
                count=count-1
                print("***left with",count,"attempts***")
            if count==0:
                print("***Your card has been blocked!!!,Please visit the Branch,Thank you.***")
                break
    else:
        print("***Sorry,Account information not found***")
    main()

def withdrawAmount():
      count = 3
      AC_NO = input('Enter your AC_NO:')
      mycursor = mydb.cursor()
      mycursor.execute("select*from account where AC_NO=%s;", (AC_NO,))
      data = mycursor.fetchall()
      if data:
          while True:
              PASSWORD = input('Enter your PASSWORD:')
              mycursor.execute("select*from account where PASSWORD=%s;", (PASSWORD,))
              data = mycursor.fetchall()
              if data:
                  AMOUNT = int(input("Please enter the amount to withdraw:"))
                  mycursor.execute('update account set Balance = Balance-%s;',(AMOUNT,))
                  mydb.commit()
                  print("***Transaction completed successfully***")
                  break
              else:
                  print("***Wrong pin!!,Please try Again ***")
                  count = count - 1
                  print("***left with", count, "attempts***")
              if count == 0:
                  print("***Your card has been blocked!!!,Please visit the Branch,Thank you.***")

      else:
          print("***Sorry,Account information not found***")

      main()

def closeAccount():
    AC_NO = input('Enter customer AC_NO:')
    PASSWORD = input('Enter your PASSWORD:')
    mycursor = mydb.cursor()
    mycursor.execute("select*from account where AC_NO=%s and PASSWORD=%s;", (AC_NO, PASSWORD))
    data=mycursor.fetchone()
    if data:
        mycursor.execute("select*from account where AC_NO=%s and PASSWORD=%s;",(AC_NO, PASSWORD))
        print("Account closed successfully")
    else:
        print("something went wrong")
    main()
def changePassword():
    AC_NO = input('Enter customer AC_NO:')
    PASSWORD = input('Enter your PASSWORD:')
    mycursor = mydb.cursor()
    mycursor.execute("select*from account where AC_NO=%s and PASSWORD=%s;", (AC_NO, PASSWORD))
    data = mycursor.fetchone()
    if data:
        NewPASSWORD=input("Enter new password:")
        mycursor.execute('update account set PASSWORD =%s;',(NewPASSWORD,))
        mydb.commit()
        print("*** YOUR PASSWORD CHANGED SUCCESSFULLY ***")
    else:
        print("***Sorry! Account information not found,Please try again***")
    main()
def help():
    print("Please, Visit The Official Website !!!")
    main()
def main():
    print("----------------------------------------------")
    print("-         ATM MANAGEMENT SYSTEM              -")
    print("----------------------------------------------")
    print("1.NEW CUSTOMER")
    print("2.SEARCH ACCOUNT")
    print("3.DEPOSIT AMOUNT")
    print("4.WITHDRAW AMOUNT")
    print("5.CLOSE ACCOUNT")
    print("6.CHANGE PASSWORD")
    print("7.HELP")
    choice = int(input("\n Please Enter Your Choice : "))
    if choice == 1:
       newCustomer()
    elif choice == 2:
       searchAccount()
    elif choice == 3:
       depositAmount()
    elif choice == 4:
        withdrawAmount()
    elif choice == 5:
        closeAccount()
    elif choice == 6:
        changePassword()
    elif choice == 7:
        help()
    else:
        print("Wrong input!!!")
main()
