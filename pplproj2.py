# from ast import For
from msvcrt import getch
import mysql.connector  as mysql 
import smtplib
from email.message import EmailMessage
# import datetime as dt
from colorama import init, Fore, Style
import os
import getpass

init()

s=1
while s==1:
    s=0
    try:
        db = mysql.connect(host="localhost",user="root",password="",database="hostel")
        command_handler= db.cursor(buffered=True)
    except:
        print(Fore.LIGHTRED_EX+"Something went wrong, could not connect to database!")
        getch()
        s=1

def auth_admin():
    print("\nrector login")
    username=input("username: ")
    password=getpass.getpass("password: ")
    if username == "admin":
        if password=="password":
            os.system('cls')
            rector_session()
        else: print(Fore.LIGHTRED_EX+"incorrect password!\n")
    else: print(Fore.LIGHTRED_EX+"login details not recognized\n")
    getch()

def studentSection():
    while 1:
        os.system('cls')
        print(Fore.YELLOW+ "Student Section\n---------------------------------------",Style.RESET_ALL)
        print("1. register student")
        print("2. apply for leave")
        print("3. change leave stat")
        print("4. mail")
        print("5. view details")
        print("6. search student by vehicle no.")
        # print("7. register worker")
        # print("9. enter expenses")
        print("7. select student by admission ending month")
        print("8. select student by room no.")
        print("0. exit")
        opt=input("\nchoose option: "+Fore.LIGHTRED_EX)
        print(Style.RESET_ALL+"")
        if opt=='1':
            username=input("student name:             ")
            mono=input("mobile no.:               ")
            mail=input("mail:                     ")
            roomno=input("room no.:                 ")
            place=input("place:                    ")
            p1name=input("p1 name:                  ")
            p1mono=input("p1 mobile no.:            ")
            p1mail=input("p1 mail:                  ")
            admsm=input("admission starting month: ") 
            admem=input("admission ending month:   ")
            vhcno=input("vehicle no.:              ")
            locgrdno=input("local gaurdian no.:       ")
            edu=input("education:                ")
            clg=input("college:                  ")
            comment=input("comment:                  ")
            addr=input("address:                 ")
            feespaid=input("fess paid:                ")
            admstat=1
            rtdt='-'
            
            query_vals = (username,mono,mail,roomno,place,p1name,p1mono,p1mail,admsm,admem,vhcno,locgrdno,edu,clg,comment,addr,feespaid,admstat)
            try:
                command_handler.execute( "INSERT INTO users (username,mono,mail,roomno,place,p1name,p1mono,p1mail,admsm,admem,vhcno,locgrdno,edu,clg,comment,addr,feespaid,admstat) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",query_vals)
                db.commit()
                command_handler.execute("SELECT roll FROM users WHERE username=%s",(username,))
                i=command_handler.fetchone()
                i=str(i)
                print("\ndone! the roll number of user is",Fore.YELLOW,i[1:len(i)-2],"\n")
            except:
                print(Fore.LIGHTRED_EX+"incorrect data input!")

        elif opt=="2":
            if __name__ == '__main__':
                rn=input("roll no.: ")
                rnt=(rn,)
                command_handler.execute("SELECT p1mail FROM users WHERE roll=%s",rnt)
                s2=command_handler.fetchone()
                command_handler.execute("SELECT username FROM users WHERE roll=%s",rnt)
                un=str(command_handler.fetchone())
                un=un[2:len(un)-3]
                n=input("nights: ")
                where=input("where: ")
                why=input("why: ")
                date=(input("return date: "))
                s1='{} has applied for a leave for {} nights and will be going to {}.\nreson: {}\nreturn date: {}'.format(un,n,where,why,date)
                email_alert("student applied for leave",s1,s2)
                query_val=(date,rn)
                try:
                    command_handler.execute("UPDATE users SET rtdt=%s WHERE roll=%s",query_val)
                    db.commit()
                    print(Fore.YELLOW+"\nalert sent!")
                except:
                    print(Fore.LIGHTRED_EX+"incorrect data input!")


        elif opt=="3":
            rn=input("roll no.: ")
            command_handler.execute("SELECT rtdt FROM users WHERE roll=%s",(rn,))
            i=str(command_handler.fetchone())
            # print(i)
            if i!='None':
                print("return date was: ",i[2:len(i)-3])
                print("press 1 to msg; enter to continue!")
                inp=input()
                if inp=='1':
                    command_handler.execute("SELECT p1mail FROM users WHERE roll=%s",(rn,))
                    mail=command_handler.fetchone()
                    mail=str(mail)
                    mail=mail[2:len(mail)-3]
                    # print(mail)
                    email_alert("Student reported late","student has reported today for last leave wherin he was supposed to return at {}".format(i),mail)    
                command_handler.execute("UPDATE users SET rtdt='-' WHERE roll={}".format(rn))
                db.commit()
                print(Fore.YELLOW+"status updated\n")
            else:
                print(Fore.LIGHTRED_EX+'no user with roll number ',rn)
        
        elif opt=="4":
            print("1. all parents")
            print("2. some students")
            print("3. some parents")
            print("4. some stdnts and prnts")
            user_opt=input("\nchoose opt: "+Fore.LIGHTRED_EX)
            if user_opt=='1':
                # for i in rn:
                mailids=""
                command_handler.execute("SELECT p1mail FROM users")
            
                i=command_handler.fetchall()
                for j in i:
                # print(j)
                    j=str(j)
                    j=j[2:len(j)-3]
                    mailids+=j
                    mailids+=','
                # mailids=mailids[:-1]
                # print(mailids)
                mailids=mailids[:-1]
                # print(mailids)
                s1=input(Style.RESET_ALL+"msg: ")
                print("sending....")
                email_alert("NOTICE FROM HOSTEL",s1,mailids)
                print(Fore.YELLOW+"email sent")
        
            elif user_opt=='2' or user_opt=='3' or user_opt=='4':
                rn=tuple(input(Style.RESET_ALL+"roll no.: ").split())
                mailids=""
                if user_opt=='3':
                    # rn=tuple(input("roll no.: ").split())
                    # mailids=""
                    # print("a")
                    for i in rn:
                        # print("b")
                        command_handler.execute("SELECT p1mail FROM users WHERE roll=%s",(i,))
                        j=command_handler.fetchone()
                        j=str(j)
                        j=j[2:len(j)-3]
                        mailids+=j
                        mailids+=','
                elif user_opt=='2':
                    # rn=tuple(input("roll no.: ").split())
                    #mailids=""
                    for i in rn:
                        command_handler.execute("SELECT mail FROM users WHERE roll=%s",(i,))
                        j=command_handler.fetchone()
                        j=str(j)
                        j=j[2:len(j)-3]
                        mailids+=j
                        mailids+=','
                elif user_opt=='4':
                    # rn=tuple(input("roll no.: ").split())
                    # mailids=""
                    for i in rn:
                        command_handler.execute("SELECT mail FROM users WHERE roll=%s",(i,))
                        j=command_handler.fetchone()
                        j=str(j)
                        j=j[2:len(j)-3]
                        mailids+=j
                        mailids+=','
                        command_handler.execute("SELECT p1mail FROM users WHERE roll=%s",(i,))
                        j=command_handler.fetchone()
                        j=str(j)
                        j=j[2:len(j)-3]
                        mailids+=j
                        mailids+=','
                    # print(mailids)
                mailids=mailids[:-1]
                # print(mailids)
                s1=input(Style.RESET_ALL+"msg: ")
                email_alert("NOTICE FROM HOSTEL",s1,mailids)
                print(Fore.YELLOW+"email sent")

            else:
                print(Fore.LIGHTRED_EX+"invalid input")
                getch()
                studentSection()        

        elif opt=='5':
            rn=input("roll no. or name: "+Fore.LIGHTRED_EX)
            if rn:
                rnt=(rn,)
                try:
                    tmp=int(rn)
                # print(type(rn))
                    command_handler.execute("SELECT username,mono, mail, roomno, p1name, p1mono, feespaid FROM users WHERE roll=%s",rnt)
                    s2=command_handler.fetchall()
                    if s2:
                        print(Style.RESET_ALL+"Name:      ",s2[0][0])
                        print("Mobile:    ",s2[0][1])
                        # print("Mail:      ",s2[0][2])
                        print("Room no.:  ",s2[0][3])
                        print("P1 name:   ",s2[0][4])
                        print("P1 mobile: ",s2[0][5])
                    else: print(Fore.LIGHTRED_EX+"no user with roll no.",rn)
                except:
                    command_handler.execute("SELECT username,mono, mail, roomno, p1name, p1mono, feespaid FROM users WHERE username like '%{}%'".format(rn))
                    s2=command_handler.fetchall()
                    if s2:
                        print(Style.RESET_ALL+"Name:      ",s2[0][0])
                        print("Mobile:    ",s2[0][1])
                        # print("Mail:      ",s2[0][2])
                        print("Room no.:  ",s2[0][3])
                        print("P1 name:   ",s2[0][4])
                        print("P1 mobile: ",s2[0][5])
                    else: print(Fore.LIGHTRED_EX+"no user with name",rn)
            else: print(Fore.LIGHTRED_EX+"plz give correct input")

        elif opt=="6":
            vno=input("vehicle no.: ")
            command_handler.execute("SELECT username FROM users WHERE vhcno=%s",(vno,))
            i=command_handler.fetchone()
            i=str(i)
            if i=='None':
                print(i)
            else:
                print(i[2:len(i)-3])
                command_handler.execute("SELECT mono FROM users WHERE vhcno=%s",(vno,))
                i=command_handler.fetchone()
                i=str(i)
            # print(i)
                print(i[1:len(i)-2],"\n")
            # i=str(i)
            # print("\ndone! the roll number of user is",i,"\n")
    
        elif opt=='7':
            command_handler.execute("SELECT roll, username, mono FROM users WHERE admem=%s",(input("enter month: "),))
            out=command_handler.fetchall()
            print(out)

        elif opt=='8':
            command_handler.execute("SELECT roll,username,edu FROM users WHERE roomno={}".format(input("enter room no.: "+Fore.LIGHTRED_EX)))
            out=command_handler.fetchall()
            print(Style.RESET_ALL,out)
        
        elif opt=="0":
            break

        getch()
        


def rector_session():
    print(Fore.YELLOW+ "\nlogin success; welcome rector")
    while 1:
        print(Fore.YELLOW+ "---------------------------------------",Style.RESET_ALL)
        print("1. student section")
        print("2. view worker details")
        print("3. enter expenses")
        print("4. register worker")
        print("0. logout")

        user_option=input("\nchoose opt: "+Fore.LIGHTRED_EX)
        print(Style.RESET_ALL+"")
        if user_option=="1":
            studentSection()
        
        elif user_option=='2':
            rn=input("name.:   "+Fore.LIGHTRED_EX)
            command_handler.execute("SELECT mono, bankacno, ifsc FROM staff WHERE name like '{}%'".format(rn))
            s2=command_handler.fetchall()
            if s2:    
                print(Style.RESET_ALL+"Mobile:      ",s2[0][0])
                print("bank ac no.: ",s2[0][1])
                # print("Mail:      ",s2[0][2])
                print("ifsc:        ",s2[0][2])
                getch()
            else: print(Fore.LIGHTRED_EX+"no worker with name ",rn)
            getch()
            # print("locgrdno:  ",s2[0][6])
            # print("feespaid:  ",s2[0][10],"\n")
            # os.system('cls')

        elif user_option=='3':
            month=input("month: ")
            wbill=input("Water bill: ")
            ebill=input("Electricity bill: ")
            taxes=input("Taxes: ")
            wsalary=input("Woker salary:")
            food=input("food: ")
            maintanence=input("Maintanence: ")
            special_comment=input("Special comment: ")
            try:
                total=int(wbill)+int(ebill)+int(taxes)+int(wsalary)+int(food)+int(maintanence)
                query_vals=(month,ebill,wbill,taxes,wsalary,food,maintanence,special_comment,total)
                command_handler.execute("INSERT INTO expenses (month,ebill,wbill,tax,salary,food,maintenance,comment,total) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",query_vals)
                db.commit()
                print("added expenses for",Fore.YELLOW+month,"month.\n")
            except:
                print(Fore.LIGHTRED_EX+"incorrect data input!")
            getch()

        elif user_option=="4":
            name=input("worker name: ")
            mono=input("mobile no.: ")
            bankacno=input("bank acc no.: : ")
            ifsc=input("ifsc: ")
            addr=input("address: ")
            mail=input("mail: ")
            joindt=input("joining month: ") 
            vhcno=input("vehicle no.: ")
            edu=input("education: ")
            comment=input("comment : ")        
            query_vals = (name,mono,bankacno,ifsc,addr,mail,joindt,vhcno,edu,comment)
            command_handler.execute("INSERT INTO staff (name, mono, bankacno, ifsc, addr, mail, joindt, vhcno, edu, comment) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",query_vals)
            db.commit()
            print(Fore.YELLOW+"\ndone")
            getch()

        elif user_option=="0":
            break

        os.system('cls')
        

def email_alert(subject, body, to):
    msg= EmailMessage()
    msg.set_content(body)
    msg['subject']=subject
    msg['to']=to

    user = ""
    msg['from']=user
    password=""
    try:
        server=smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        # print("a")
        server.login(user,password)
        # print("b")
        server.send_message(msg)
        server.quit()
    except:
        print(Fore.LIGHTRED_EX+"Something went wrong, email not sent!")

def main():
    while 1:
        os.system('cls')
        print(Fore.YELLOW+ "---------------------------------------",Style.RESET_ALL)
        print(Fore.YELLOW+ "welcome to hostel system",Style.RESET_ALL)
        auth_admin()
        # admin_session()

main()
    
