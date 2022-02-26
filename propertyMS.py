from tkinter import *
from tkinter import ttk
import mysql.connector
import tkinter.messagebox


class ConnectorDB:

    def __init__(self,root):
        self.root = root
        titlespace = " "
        self.root.title(102*titlespace +"MySQL Connector")
        self.root.geometry("895x700+300+0")
        self.root.resizable(width =False, height =False)

        MainFrame = Frame(self.root, bd=10, width=770, height=700, relief=RIDGE, bg='cadet blue')
        MainFrame.grid()

        TitleFrame = Frame(MainFrame, bd=7, width=770, height=100, relief=RIDGE)
        TitleFrame.grid(row = 0, column = 0)
        Topframe3 = Frame(MainFrame,bd=5,width=770,height=500,relief =RIDGE)
        Topframe3.grid(row = 1, column = 0)

        LeftFrame = Frame(Topframe3, bd=5, width=770, height=400, padx=2, relief=RIDGE, bg ="cadet blue")
        LeftFrame.pack(side =LEFT)
        LeftFrame1 = Frame(LeftFrame, bd=5, width=600, height=180,padx=12,pady=9, relief=RIDGE)
        LeftFrame1.pack(side = TOP)

        RightFrame1 = Frame(Topframe3, bd=5, width=100, height=400, padx=2, bg ="cadet blue", relief=RIDGE)
        RightFrame1.pack(side =RIGHT)
        RightFrame1a = Frame(RightFrame1, bd=5, width=90, height=300,  padx=2,pady=2,relief=RIDGE)
        RightFrame1a.pack(side = TOP)

        #===================================================================================================
        Address =StringVar()
        Price=StringVar()
        Date=StringVar()
        City= StringVar()
        State=StringVar()
        Country=StringVar()
        ID=StringVar()

        #===================================================================================================

        def iExit():
            iExit= tkinter.messagebox.askyesno("Property Management System","Confirm if you want to exit")
            if iExit > 0:
                root.destroy()
                return

        def Reset():

            self.entpropertyID.delete(0, END)
            self.entpropertyAddress.delete(0, END)
            self.entpropertyPrice.delete(0, END)
            self.entpropertyDate.delete(0, END)
            self.entpropertyCity.delete(0, END)
            self.entpropertyState.delete(0, END)
            self.entpropertyCountry.delete(0, END)
            self.entpropertyID.delete(0, END)


        def addData():
            if  ID.get() == "" or Address.get() =="" or Price.get() =="" or Date.get() =="" or City.get() =="" or State.get() =="" or Country.get() =="":
                tkinter.messagebox.showerror("Property Management System", "Enter Correct Details")
            else:
                sqlCon = mysql.connector.connect(host="localhost",user="root",password="",database="project")
                cur=sqlCon.cursor()

                cur.execute("insert into property values (%s)" % ID.get())

                cur.execute("insert into location (ID,address,city,state,country) values (%s,%s,%s,%s,%s)",(ID.get(),Address.get(),City.get(),State.get(),Country.get()))
                cur.execute("insert into attributes (ID,price,date) values (%s,%s,%s)",(ID.get(),Price.get(),Date.get()))

                sqlCon.commit()
                DisplayData()
                sqlCon.close()
                tkinter.messagebox.showinfo("Property Management System", "Record Entered Successfully")

        def DisplayData():

            sqlCon = mysql.connector.connect(host="localhost", user="root", password="",
                                                 database="project")
            cur = sqlCon.cursor()
            cur.execute("""select property.ID,location.address,attributes.price,attributes.date,location.city,location.state,location.country 
                        from property 
                        inner join location on location.ID = property.ID inner join attributes on property.ID = attributes.ID""")
            result = cur.fetchall()

            if len(result) != 0:
                self.properties_records.delete(*self.properties_records.get_children())
                for row in result:
                    self.properties_records.insert('',END,values=row)
                    sqlCon.commit()
            sqlCon.close()

        def PropertyInfo(ev):
            viewinfo =self.properties_records.focus()
            propertyData =self.properties_records.item(viewinfo)
            row = propertyData['values']

            ID.set(row[0])
            Address.set(row[1])
            Price.set(row[2])
            Date.set(row[3])
            City.set(row[4])
            State.set(row[5])
            Country.set(row[6])




        def Update():
            sqlCon = mysql.connector.connect(host="localhost", user="root", password="",
                                             database="project")
            cur = sqlCon.cursor()
            cur.execute(" update location set address = %s, city = %s , state = %s , country = %s where ID = %s ", (Address.get(),
                        City.get(),State.get(), Country.get(),ID.get()))
            cur.execute( "update attributes set price = %s , date = %s where ID = %s ", (Price.get(),Date.get(),ID.get()))
            sqlCon.commit()
            DisplayData()
            sqlCon.close()

            tkinter.messagebox.showinfo("Property Management System", "Record Updated Successfully")

        def Delete():
            sqlCon = mysql.connector.connect(host="localhost", user="root", password="",
                                             database="project")
            cur = sqlCon.cursor()
            cur.execute("delete attributes.* from attributes where attributes.ID = %s" % ID.get())
            cur.execute("delete location.* from location where location.ID = %s" % ID.get())
            cur.execute("delete property.* from property where property.ID = %s" % ID.get())
            sqlCon.commit()
            selected_item = self.properties_records.selection()[0]  ## get selected item
            self.properties_records.delete(selected_item)
            sqlCon.close()
            tkinter.messagebox.showinfo("Property Management System", "Record Deleted Successfully")
            Reset()


        def Search():
            try:
                sqlCon = mysql.connector.connect(host="localhost", user="root", password="",
                                                 database="project")
                cur = sqlCon.cursor()
                cur.execute("""select property.ID ,location.address, attributes.price ,attributes.date,location.city,location.state,location.country 
                            from property inner join location
                            on location.ID = property.ID inner join attributes on attributes.ID = property.ID where property.ID = %s """ % ID.get())

                row = cur.fetchone()


                Address.set(row[1])
                Price.set(row[2])
                Date.set(row[3])
                City.set(row[4])
                State.set(row[5])
                Country.set(row[6])


                sqlCon.commit()

            except:

                tkinter.messagebox.showinfo("Property Management System", "No Such Record Found")
                Reset()
            sqlCon.close()

        #===================================================================================================

        self.lbltitle = Label(TitleFrame, font=('arial',25,'bold'),text="PROPERTY MANAGEMENT SYSTEM",bd =7)
        self.lbltitle.grid(row=0,column=0,padx=132)

        self.lblpropertyID = Label(LeftFrame1, font=('arial', 12, 'bold'), text="Property ID :", bd=7)
        self.lblpropertyID.grid(row=1, column=0, sticky=W, padx=5)
        self.entpropertyID = Entry(LeftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left',
                                   textvariable=ID)
        self.entpropertyID.grid(row=1, column=1, sticky=W, padx=5)
        self.entpropertyID.grid(row=1, column=1, sticky=W, padx=5)

        self.lblpropertyAddress = Label(LeftFrame1, font=('arial', 12, 'bold'), text="Address :", bd=7)
        self.lblpropertyAddress.grid(row=2, column=0, sticky=W, padx=5)
        self.entpropertyAddress = Entry(LeftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left',textvariable=Address)
        self.entpropertyAddress.grid(row=2, column=1, sticky=W, padx=5)

        self.lblpropertyPrice = Label(LeftFrame1, font=('arial', 12, 'bold'), text="Price :", bd=7)
        self.lblpropertyPrice.grid(row=3, column=0, sticky=W, padx=5)
        self.entpropertyPrice = Entry(LeftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left',textvariable=Price)
        self.entpropertyPrice.grid(row=3, column=1, sticky=W, padx=5)

        self.lblpropertyDate = Label(LeftFrame1, font=('arial', 12, 'bold'), text="Date :", bd=7)
        self.lblpropertyDate.grid(row=4, column=0, sticky=W, padx=5)
        self.entpropertyDate = Entry(LeftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left',textvariable=Date)
        self.entpropertyDate.grid(row=4, column=1, sticky=W, padx=5)

        self.lblpropertyCity = Label(LeftFrame1, font=('arial', 12, 'bold'), text="City :", bd=7)
        self.lblpropertyCity.grid(row=5, column=0, sticky=W, padx=5)
        self.entpropertyCity = Entry(LeftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left',textvariable=City)
        self.entpropertyCity.grid(row=5, column=1, sticky=W, padx=5)

        self.lblpropertyState = Label(LeftFrame1, font=('arial', 12, 'bold'), text="State :", bd=7)
        self.lblpropertyState.grid(row=6, column=0, sticky=W, padx=5)
        self.entpropertyState = Entry(LeftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left',textvariable=State)
        self.entpropertyState.grid(row=6, column=1, sticky=W, padx=5)

        self.lblpropertyCountry = Label(LeftFrame1, font=('arial', 12, 'bold'), text="Country :", bd=7)
        self.lblpropertyCountry.grid(row=7, column=0, sticky=W, padx=5)
        self.entpropertyCountry = Entry(LeftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left',textvariable=Country)
        self.entpropertyCountry.grid(row=7, column=1, sticky=W, padx=5)


        #======================================================Table Treeview=================================================

        scroll_y=Scrollbar(LeftFrame, orient =VERTICAL)
        scroll_x = Scrollbar(LeftFrame, orient=HORIZONTAL)

        self.properties_records=ttk.Treeview(LeftFrame, height = 12, columns =("ID","Address","Price","Date","City","State","Country") , yscrollcommand =scroll_y.set,xscrollcommand=scroll_x.set)

        scroll_y.pack(side = RIGHT, fill = Y)
        scroll_x.pack(side=BOTTOM,fill = X)

        self.properties_records.heading("ID", text="Property ID")
        self.properties_records.heading("Address", text="Address")
        self.properties_records.heading("Price", text="Price")
        self.properties_records.heading("Date", text="Date")
        self.properties_records.heading("City", text="City")
        self.properties_records.heading("State", text="State")
        self.properties_records.heading("Country", text="Country")


        self.properties_records['show']='headings'

        self.properties_records.column("ID", width=70)
        self.properties_records.column("Address", width=120)
        self.properties_records.column("Price", width=70)
        self.properties_records.column("Date", width=70)
        self.properties_records.column("City", width=70)
        self.properties_records.column("State", width=70)
        self.properties_records.column("Country", width=70)


        self.properties_records.pack(fill = BOTH, expand=1)
        self.properties_records.bind("<ButtonRelease-1>",PropertyInfo)


        #=================================================================================

        self.btnAddNew=Button(RightFrame1a,font=('arial',16,'bold'),text="Add New", bd=4 ,pady=1,padx=24,
                                width = 8,height =2,command=addData).grid(row=0,column=0,padx=1)
        self.btnDisplay = Button(RightFrame1a, font=('arial', 16, 'bold'), text="Display", bd=4, pady=1, padx=24,
                                width=8,height=2,command=DisplayData).grid(row=1, column=0, padx=1)
        self.btnUpdate = Button(RightFrame1a, font=('arial', 16, 'bold'), text="Update", bd=4, pady=1, padx=24,
                                width=8,height=2,command=Update).grid(row=2, column=0, padx=1)
        self.btnDelete = Button(RightFrame1a, font=('arial', 16, 'bold'), text="Delete", bd=4, pady=1, padx=24,
                                width=8,height=2, command = Delete).grid(row=3, column=0, padx=1)
        self.btnSearch = Button(RightFrame1a, font=('arial', 16, 'bold'), text="Search", bd=4, pady=1, padx=24,
                                width=8,height=2,command = Search).grid(row=4, column=0, padx=1)
        self.btnReset = Button(RightFrame1a, font=('arial', 16, 'bold'), text="Reset", bd=4, pady=1, padx=24,
                                width=8,height=2,command=Reset).grid(row=5, column=0, padx=1)
        self.Exit = Button(RightFrame1a, font=('arial', 16, 'bold'), text="Exit", bd=4, pady=1, padx=24,
                                width=8,height=2,command=iExit).grid(row=6, column=0, padx=1)






if __name__ =='__main__':
    root  = Tk()
    application = ConnectorDB(root)
    root.mainloop()
