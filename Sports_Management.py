# First of all we import the necesaary modules
# Then that we connet our program to MYSQL
# After that we create a function which calls the data from mysql to python and call it
# After it we create the sub-functions which will be called by the main function 
# After it we create the main function thorugh which our program runs
# In last after the welcome line we calls our main function

#importing statements
import mysql.connector as msc
import pandas as pd
from datetime import datetime
import numpy as np
from fpdf import FPDF
import os
import matplotlib.pyplot as plt

# Here we used try-except conditional statements
try:
    # We ask user his/her mysql password for making connection of program to mysql
    mysql_paswrd = input("Enter password of your MySQL: ")

    # Here we tried to connect in existing parking database in this try loop if it was created previously
    mysql_obj = msc.connect(host = "localhost",
                            user = "root",
                            passwd = mysql_paswrd,
                            database = "Sports_Management",
                            charset = 'utf8')
    mysql_crsr = mysql_obj.cursor()
    mysql_crsr.execute("use Sports_Management;")
except:
    # If database would not found then we create a new database in this except loop    
    mysql_obj = msc.connect(host = "localhost",
                            user = "root",
                            passwd = mysql_paswrd,
                            database = "mysql",
                            charset = 'utf8')
    mysql_crsr = mysql_obj.cursor()
    mysql_crsr.execute("create database Sports_Management;")
    mysql_crsr.execute("use Sports_Management;")

    # Here we create parking-management table
    mysql_crsr.execute("create table Equipments(Item_ID int Primary Key, Item_Name varchar(54) ,Brand varchar(54),Total_Items int,Items_Now int);")
    # We add some dumy data here
    mysql_crsr.execute("insert into Equipments values(1, 'Football', 'Nivia', 10, 10),(2, 'Badminton Racket', 'Yonex', 20, 17),(3, 'Cricket Bat', 'Rebook', 12, 12),(4, 'Baseball Bat', 'Cosco', 4, 4),(5, 'Chess Set', 'Matrix', 4, 4),(6, 'Skipping Rope', 'Adidas', 12, 12),(7, 'Skates', 'Nike', 5, 4),(8, 'Hand Ball', 'Cosco', 4, 2),(9, 'Volly Ball', 'Cosco', 7, 6),(10, 'Basket Ball', 'Cosco', 8, 8);")

    # Here we create vechile-categories table
    mysql_crsr.execute("create table Lend_Data(Lending_No int Primary Key, Name varchar(48),Class varchar(6), Roll_No varchar(3), Lending_Time datetime, Returning_Time datetime,Item_ID int, Quantity int, Status varchar(20));")
    # Inserting data in vechile-category table
    mysql_crsr.execute("insert into Lend_Data values(1, 'Rahul', '8', '32', '2021-01-06 10:20:20', '2021-01-07 11:40:50', 2, 1,'Returned'),(2, 'Rani', '10', '26', '2021-01-12 12:20:20', '2021-01-15 16:04:10', 1, 1,'Returned'),(3, 'Mahima', '12', '37','2021-01-15 15:39:41', '2021-01-15 16:04:10', 5, 1,'Returned'),(4, 'Nupur', '1', '16','2021-01-15 15:42:16', '2021-01-15 16:04:10', 6, 1,'Returned'),(5, 'Heena', '10', '31','2021-01-15 15:46:10', '2021-01-15 16:04:10', 8, 1,'Returned'),(6, 'Aman', '9', '2','2021-01-15 15:53:03', '0000-00-00 00:00:00', 8, 1,'Owned'),(7, 'Neha', '4', '23','2021-01-15 15:56:09', '0000-00-00 00:00:00', 2, 1,'Owned'),(8, 'China', '8', '12','2021-01-15 15:57:27', '0000-00-00 00:00:00', 2, 1,'Owned'),(9, 'Geeta', '6', '19','2021-01-15 15:59:14', '0000-00-00 00:00:00', 7, 1,'Owned'),(10, 'Kritika', '12', '28','2021-01-15 16:01:01', '0000-00-00 00:00:00', 2, 1,'Owned'),(11, 'Priya', '5', '32','2021-01-15 16:02:28', '0000-00-00 00:00:00', 8, 1,'Owned'),(12, 'Diksha', '9', '26','2021-01-15 16:04:10', '0000-00-00 00:00:00', 9, 1,'Owned'),(13, 'Akansha', '7', '4','2021-01-15 16:13:45.293137', '0000-00-00 00:00:00', 6, 1,'Owned');")

    #For saving all the above creation/changes in MySQL permanently
    mysql_obj.commit()

# Here we define this function that calls data from mysql server
def fetch_mysql():
    mysql_crsr.execute("select * from Equipments;")
    # As variables in def function are local so we have to make them gloabal for using them outside the def
    global equipments_data
    equipments_data = mysql_crsr.fetchall()
    mysql_crsr.execute("select * from Lend_Data;")
    global lending_data
    lending_data = mysql_crsr.fetchall()

# We call the above function, as the function defining below use the data from mysql that is introduced above
fetch_mysql()

# We define this sub-function of main function which runs on main function call, this function will do the functionality of main-function i.e. View  sports equipments records - 1st
def equipment_records():
    # Converting the fetched data from mysql into tabluar form to show
    equipments_table = pd.DataFrame(equipments_data, columns=['Item_ID', 'Item_Name','Brand','Total_Items','Items_Now'])
    print("\nEquipments Records....\n")
    print(equipments_table)
    print("\n")

    # After completion of this function we call the main function in it so that it will run unbreakably
    main_function()

# This is sub-function of main function which runs on main function call, this function will do the functionality of main-function i.e. View  sports lending records - 2nd
def lending_records():
    # Converting the fetched data from mysql into tabluar form to show
    lending_table = pd.DataFrame(lending_data, columns=['Lending_No', 'Name' ,'Class', 'Roll_No', 'Lending_Time', 'Returning_Time', 'Item_ID', 'Quantity', 'Status'])
    print("\nLending Records....\n")
    print(lending_table)
    print("\n")
    main_function()

# This is sub-function of main function which runs on main function call, here we define the functionality i.e. adding new entery in lending records - 3rd
def lending_entery():
    print("\nLending Entery....\n")

    # Here we ask necessary details from user of student
    student_name = input("Enter name of student : ")
    student_class = input("Enter class of student : ")
    student_roll_No = input("Enter roll number of student : ")
    
    # Here first we genrate the new entery data values like Lending_No, Lending_Time, Returning_Time, Status
    # This data helps us to genrate the next Lending_No
    Lending_No = lending_data[-1][0]+1

    # Here we genrate the new entery data values like Lending_Time
    lending_time = datetime.now()

    # Here we show user this table to opt the item which is avilable now and take choice from user
    equipments_table = pd.DataFrame(equipments_data, columns=['Item_ID', 'Item_Name','Brand','Total_Items','Items_Now'])
    print(equipments_table)
    Item_ID = input("\nEnter the equipment id from table which you wants to give: ")

    # This variable stores the quantity that are avilabe in stock of that particular demanding equipment
    item_id_array = np.array(np.arange(1, len(equipments_data)+1), dtype='U')

    # Here we check the input vale can be feasiable or not
    if Item_ID in item_id_array:
        # Here we check the required item is avilabe or not
        def stock_checker():
            global quantity
            quantity = input("Enter the quantity of equipment that you are lending: ")
            try:
                # First we check the no. is integer or not
                quantity = int(quantity)
            except:
                # Then we re-call the function requesting to enter correct value
                print("\nPlease enter a valid number\n")
                stock_checker()
            if quantity <= equipments_data[int(Item_ID)-1][4]:
                # Here all the conditions are verified so we updated mysql server too
                mysql_crsr.execute(f"update equipments set Items_Now = {equipments_data[int(Item_ID)-1][4]-quantity} where Item_ID = {Item_ID};")
            else:
                # This notifies that eqiupments are not avilable in stock
                print(f"\nStock have only {equipments_data[int(Item_ID)-1][4]} {equipments_data[int(Item_ID)-1][1]}\n")
                stock_checker()
        stock_checker()

        # Here we update the lend_data table of mysql by adding new entery in it
        mysql_crsr.execute(f"insert into Lend_Data values({Lending_No}, '{student_name}', '{student_class}', '{student_roll_No}','{lending_time}', '0000-00-00 00:00:00', {Item_ID}, {quantity},'Owned');")
        mysql_obj.commit()

        #Lending Slip Genration in PDF Format
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial" ,size=20)

        # This cell method will create the line in pdf page
        pdf.cell(0,25,"KENDRIYA VIDAYALAYA NO.4 JAIPUR SPORTS CLUB", ln=1, align="C")
        pdf.cell(0,4,"Sports Equipment Lending Recipt", ln=1, align="C")
        pdf.set_font("Arial","B" ,size=18)
        pdf.cell(0,40,f"Lending ID : {Lending_No}",ln=1,align="L")

        # This code changes the font aspects from here that will we written in PDF
        pdf.set_font("Arial", size=16)
        pdf.cell(0,0,f"Student Name : {student_name}",ln=0,align="L") 
        pdf.cell(0,0,f"Date : {datetime.strftime(lending_time,'%d-%m-%y')}",ln=1,align="R")
        pdf.cell(0,20,f"Student Class : {student_class}",ln=0,align="L")  
        pdf.cell(0,20,f"Time : {datetime.strftime(lending_time,'%H:%M:%S')}",ln=1,align="R")
        pdf.cell(0,0,f"Student Roll Number : {student_roll_No}",ln=1,align="L")
        pdf.cell(0,20,f"Sports Item ID : {Item_ID}",ln=1,align="L")
        item_name = equipments_data[int(Item_ID)-1][2] + " " + equipments_data[int(Item_ID)-1][1]
        pdf.cell(0,0,f"Item Name : {item_name}",ln=1,align="L")
        pdf.cell(0,20,f"Sports Item Quantity : {quantity}",ln=1,align="L")
        pdf.cell(0,70,f"* Student have to take care of this slip and it is necessary to bring this slip during submission of the item.",ln=1,align="L")

        # This code make a pdf in the same loaction of program 
        pdf.output(f"Lending_slip{Lending_No}.pdf")

        # This code access the pdf file in computer location that we made above and open it
        os.startfile(f"Lending_slip{Lending_No}.pdf")

        print("\n")
        # This code will re-take data from mysql here and re-call the mysql and main function to update python with new data and make the program unbreakable
        fetch_mysql()
        main_function()
    else:
        print("\nYou entered wrong Item ID which is not existed\n")
        lending_entery()

# This is sub-function of main function which runs on main function call, here we define functionality that will do the  i.e. updating the submission of item in lending records - 4th
def submission_entery():
    # We took the user choice
    lending_id = input('Enter lending ID or enter 0 to cancel: ')
    # We verifies the user choice is integer or not
    try:
        lending_id = int(lending_id)
    except:
        print("\nPlease enter valid lending ID\n")
        submission_entery()
    if lending_id == 0:
        # This will check user want to cancel or he/she entered correct value or not
        print("\nEquipment Submission cancelled successfully\n")
        main_function()
    elif lending_id in list(range(1,len(lending_data)+1)) and lending_data[lending_id-1][-1] == 'Owned':
        # This condition will update the mysql enteries
        item_id = lending_data[lending_id-1][-3]
        Quantity = lending_data[lending_id-1][-2] + equipments_data[item_id-1][-1]
        mysql_crsr.execute(f"update equipments set Items_Now = {Quantity} where Item_ID = {item_id};")
        mysql_crsr.execute(f"update Lend_Data set Status = 'Returned' where Lending_No = {lending_id};")
        mysql_crsr.execute(f"update Lend_Data set Returning_Time = '{datetime.now()}' where Lending_No = {lending_id};")
        mysql_obj.commit()
        print("\nItem sumbited successfully in lending records\n")
    else:
        # Here user insert that value which is not in data
        print("\nPlease enter valid lending ID\n")
        submission_entery()

    print("\n")
    fetch_mysql()
    main_function()

def lending_analysis():
    print('\nEquipment lending analysis....\n')

    # Here we extract data from mysql which will be shown graphically
    mysql_crsr.execute("select e.brand,e.item_name, count(l.item_id) from lend_data l cross join equipments e on l.item_id = e.item_id group by e.item_id;")
    graph_data = mysql_crsr.fetchall()
    
    # Here we show analysis in tabular form
    statstics_table = pd.DataFrame(graph_data, columns = ["Brand","Item_Name","Lend_Quantity"])
    print(statstics_table)

    # Here we plot(make) the graph
    plt.bar(statstics_table['Item_Name'],statstics_table['Lend_Quantity'])
    plt.xlabel("Item Names")
    plt.ylabel("Number of Lending")
    plt.title("Number of Lendings accordig to Items")

    #Here we show analysis in graphical form 
    plt.show()

    print("\n")
    main_function()

#We define this main function that runs the whole program expect connectivity code
# In this we simply used a conditional loop that runs our program as per user choice
# In this conditional loop we recalls the sub functions as per user's choice
def main_function():
    print("1. View  sports equipments records\n2. View  lending records\n3. Student lending entery\n4. Student submission entery\n5. Sports Equipment Lending Analysis\n0. Quit")
    choice = input("\nEnter your choice : ")
    if choice == '0':
        print('Shuting Down...')
    elif choice == '1':
        equipment_records()
    elif choice == '2':
        lending_records()
    elif choice == '3':
        lending_entery()
    elif choice == '4':
        submission_entery()
    elif choice == '5':
        lending_analysis()
    else:
        print("\nPlease enter valid number\n")
        main_function()
        
# Here we welcome the user in our program and calls the main function
print("\nWelcome to Kenrdiya Vidyalaya No. 4 Jaipur\nSports Club Management\n\n")
main_function()