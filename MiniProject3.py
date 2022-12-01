from flask import Flask,render_template,request
import requests
import sqlite3
import pandas as pd


app = Flask(__name__)
#Home page options
@app.route('/',methods=['GET','POST'])
def home():
    return render_template("myhome.html")



#####################################  FIRST ROUTE #######################################
#Input new data first selction from home
@app.route('/dataentry',methods=['GET','POST'])
def data_entry():
    return render_template("data_entry.html")
#Shows the updated table entries and prevents empty inputs
@app.route('/tableinfo',methods=['POST'])
def table_info():
    with sqlite3.connect("mydb.db") as con:
        with open("inittable.sql") as f:
            con.executescript(f.read())
        var1 = request.form.get("name")
        var2 = request.form.get("symbol")
        var3 = request.form.get("price")
        var4 = request.form.get("code")
        if var1 == "" or var2 == "" or var3 == "" or var4 == "":
            return render_template("blank_inputs_invalidpage.html")
        #putting data into the table using a dictionary
        con.execute("INSERT INTO Inventory (Category,Descriptions,Price,Code) VALUES (:name, :description, :price, :code)",
                    {"name":var1,"description":var2,"price":var3, "code":var4})
        #viewing the table data
        df = pd.read_sql("SELECT * FROM Inventory",con)# * represents getting all the columns
        return render_template("update_inventory.html",data = df)



###################################  SECOND ROUTE #######################################
#Input what items you want to see in inventory
@app.route('/categoryretrieving',methods=['GET','POST'])
def category_retrieving():
    category = request.form.get("name")
    return render_template("retrieve_data.html")
#After picking items to see in inventory this will show those items in the inventory
@app.route('/displayinventory',methods=['POST'])
def on_hand():
    with sqlite3.connect("mydb.db") as con:
        with open("inittable.sql") as f:
            con.executescript(f.read())
        #viewing the table data
        df = pd.read_sql("SELECT * FROM Inventory",con)# * represents getting all the columns
        if request.form.get("name") == "":
            return render_template("inventory.html",data = df)
        else:
            return render_template("inventory.html",data = df.loc[df["Category"] == request.form.get("name")])




app.run(debug=True,port=8080)

