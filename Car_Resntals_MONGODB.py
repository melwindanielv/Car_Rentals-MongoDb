from tkinter import *
import pymongo

main = Tk()
main.title("MongoDB Car Rental System")


button_connect = Button(main, text="MongoDB Car Rental Database System" , bg="#008000", command=lambda:connect())
button_connect.pack(padx=40 , pady=25)

main.configure(background="#a1dbcd")
def connect():
    smain = Tk()
    smain.geometry("300x100")
    smain.configure(background="#a1dbcd")
    
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    cardb = myclient["RentCar"]
    mycars = cardb["allCars"]
    rentedcars = cardb["rentedCars"]
    label_ok = Label(smain, text="Connection Established successfully!!!...Enjoy MongoDB")
    label_ok.grid(row=8, column=6)
    smain.after(1000 , lambda: home1())
    smain.after(2000 , lambda: smain.destroy())

    def home1():
        button_addcar = Button(main, text="Add a Car to garage", bg= "#306998" , command=lambda:addcarfn())
        button_addcar.pack(padx=400, pady=25)

        button_rmcar = Button(main, text="Remove a Car from Garage", bg ="#FFD43B", command=lambda:rmcarfn())
        button_rmcar.pack(padx=400, pady=25)

        button_rent = Button(main, text="Rent a Car", bg="#FF0000", command=lambda:rentcarfn())
        button_rent.pack(padx=400, pady=25)

        button_return = Button(main, text="Return a Car",bg="#0000FF",command=lambda:retcarfn())
        button_return.pack(padx=400, pady=25)

        button_upcar = Button(main, text="Update Car Details",bg="#00FF00",command=lambda:upcarfn())
        button_upcar.pack(padx=400, pady=25)


    
    def addcarfn():
        smain = Tk()
        smain.geometry("600x300")
        smain.configure(background="#FFD43B")
        smain.title("Add Car to Garage")
        label_snum = Label(smain, fg="#FF0000" , bg="#FFD43B", text="Enter Serial Number of car")
        label_snum.grid(row=6, column=6)
        entry_snum = Entry(smain)
        entry_snum.grid(row=6, column=100)
        
        label_aname = Label(smain,fg="#FF0000" , bg="#FFD43B", text="Enter Model Name of car")
        label_aname.grid(row=8, column=6)
        entry_aname = Entry(smain)
        entry_aname.grid(row=8, column=100)

        label_mil = Label(smain, fg="#FF0000" , bg="#FFD43B", text="Enter Mileage")
        label_mil.grid(row=10, column=6)
        entry_mil = Entry(smain)
        entry_mil.grid(row=10, column=100)

        label_rnge = Label(smain, fg="#FF0000" , bg="#FFD43B", text="Enter Range")
        label_rnge.grid(row =12 , column=6)
        entry_rnge = Entry(smain)
        entry_rnge.grid(row=12 , column=100)
        
        label_ppk = Label(smain, fg="#FF0000" , bg="#FFD43B", text="Enter Price per Km")
        label_ppk.grid(row=14 , column=6)
        entry_ppk = Entry(smain)
        entry_ppk.grid(row=14 , column=100)
        

        button_submit = Button(smain, text="Add", bg="#FF0000", command=lambda:insertdb(entry_snum, entry_aname, entry_mil , entry_rnge , entry_ppk))
        button_submit.grid(row=20, column=10)

        def insertdb(snum,aname,mil,rnge,ppk):
            snum = snum.get()
            aname = aname.get()
            mil = mil.get()
            ppk = ppk.get()
            rnge = rnge.get()

            
            val = {"Serial Number":snum, "Model Name":aname, "Mileage":mil, "Range":rnge, "Price per Km":ppk}
            x = mycars.insert_one(val)
            smain.destroy()


    def rmcarfn():
        smain = Tk()
        smain.geometry("800x800")
        smain.configure(background="#306998")
        smain.title("Remove a Car from Garage")
        lbox = Listbox(smain, width=150)
        for x in mycars.find({} , {"Serial Number":1, "Model Name":1, "Mileage":1, "Range":1, "Price per Km":1}):
            x = dict(x)
            lbox.insert(1,x)
        lbox.pack()

        label_rm = Label(smain, fg="#FFD43B" , bg="#306998", text="Enter Serial number of car to remove from garage")
        label_rm.pack()

        entry_rm = Entry(smain)
        entry_rm.pack()

        button_rm = Button(smain, bg="#FFD43B", text="Remove", command=lambda:rmdb(entry_rm))
        button_rm.pack()

        def rmdb(rmsnum):
            snum = rmsnum.get()
            myquery = {"Serial Number":snum}
            mycars.delete_one(myquery)
            smain.destroy()

    def rentcarfn():
        smain = Tk()
        smain.geometry("800x800")
        smain.title("Rent a Car")
        smain.configure(background="#17A3DE")
        lbox = Listbox(smain, width=150)
        for x in mycars.find({},{"_id":0, "Serial Number":1, "Model Name":1, "Mileage":1, "Range":1, "Price per Km":1}):
            x = dict(x)
            lbox.insert(1,x)
        lbox.pack()

        label_rent = Label(smain,fg="#FF0000" , bg="#17A3DE", text="Enter Serial number of book to rent")
        label_rent.pack()

        entry_rent = Entry(smain)
        entry_rent.pack()

        button_rent = Button(smain, bg="#FF0000" , text="Rent", command=lambda:rentcar(entry_rent))
        button_rent.pack()

        def rentcar(erent):
            rent = erent.get()
            for x in mycars.find():
                if x["Serial Number"]==rent:
                    rentedcars.insert_one(x)
                    mycars.delete_one(x)
            smain.destroy()

    def retcarfn():
        smain = Tk()
        smain.geometry("800x800")
        smain.title("Return Car")
        smain.configure(background="#FFD43B")
        lbox = Listbox(smain, width=150)
        for x in rentedcars.find({},{"_id":0, "Serial Number":1,"Model Name":1, "Mileage":1 , "Range":1, "Price per Km":1}):
            x = dict(x)
            lbox.insert(1,x)
        lbox.pack()

        label_ret = Label(smain, fg="#FF0000" , bg="#FFD43B" , text="Enter Serial Number to return")
        label_ret.pack()

        entry_ret = Entry(smain)
        entry_ret.pack()

        button_ret = Button(smain, bg="#FF0000", text="Return", command=lambda:retcar(entry_ret))
        button_ret.pack()

        def retcar(eret):
            ret = eret.get()
            for x in rentedcars.find():
                if x["Serial Number"]==ret:
                    rentedcars.delete_one(x)
                    mycars.insert_one(x)
            smain.destroy()


    def upcarfn():
        smain = Tk()
        smain.geometry("600x600")
        smain.configure(background="#a1dbcd")
        smain.title("Update Car Details")
        lbox = Listbox(smain, width=150)
        for x in mycars.find({},{"_id":0, "Serial Number":1,"Model Name":1, "Mileage":1 , "Range":1, "Price per Km":1}):
            x = dict(x)
            lbox.insert(1,x)
        lbox.pack()
        
        label_snum = Label(smain, fg="#FF0000" , bg="#a1dbcd",  text="Enter Serial Number to update")
        label_snum.pack()
        entry_snum = Entry(smain)
        entry_snum.pack()

        label_mil = Label(smain, fg="#FF0000" , bg="#a1dbcd", text="Enter Mileage")
        label_mil.pack()
        entry_mil = Entry(smain)
        entry_mil.pack()

        label_rnge = Label(smain , fg="#FF0000" , bg="#a1dbcd", text="Enter Range")
        label_rnge.pack()
        entry_rnge = Entry(smain)
        entry_rnge.pack()

        label_ppk = Label(smain, fg="#FF0000" , bg="#a1dbcd" ,text="Enter Price per Km")
        label_ppk.pack()
        entry_ppk = Entry(smain)
        entry_ppk.pack()

        button_up = Button(smain, bg="#FF0000" , text="Update", command=lambda:updb(entry_snum, entry_mil, entry_rnge, entry_ppk))
        button_up.pack()

        def updb(snum, mil, rnge , ppk):
            snum = snum.get()
            mil = mil.get()
            rnge = rnge.get()
            ppk = ppk.get()

            for x in mycars.find():
                if x["Serial Number"]==snum:
                    oldval = {"Mileage":x["Mileage"], "Range":x["Range"], "Price per Km":x["Price per Km"]}
                    newval = {"$set":{"Mileage":mil, "Range":rnge, "Price per Km":ppk}}
                    mycars.update_one(oldval, newval)        
            smain.destroy()


