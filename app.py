
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, render_template, request
from mongopass import mongopass
import subprocess as sp

app = Flask(__name__)


# Create a new client and connect to the server
client = MongoClient(mongopass, server_api=ServerApi('1'))
db = client.curd
myCollection = db.myColl
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@app.route('/')
def myHome():
    date = sp.getoutput("date /t")
    return render_template("home.html", date = date)

@app.route("/curd")
def insert_val():
    return render_template("curd.html")

@app.route('/read')
def read():
    cursor = myCollection.find()
    for record in cursor:
        name = record["name"]
        print(record)
    return render_template("response.html", res = name)

@app.route('/insert')
def insert():
    name = request.args.get("name")
    address = request.args.get("address")
    myVal = {"name":name, "address":address}
    x = myCollection.insert_one(myVal)
    return render_template("response.html", res = x)

@app.route('/delete')
def delete():
    name = request.args.get("name")
    myquery = {"name":name}
    myCollection.delete_one(myquery)
    x = "Record Delete"
    return render_template("response.html", res = x)

@app.route('/update')
def update():
    name = request.args.get("name")
    new_address = request.args.get("new_address")
    myquery = {"name":name}
    newValues = {"$set": {"address": new_address}}
    myCollection.update_one(myquery, newValues)
    x = "Record Updated"
    return render_template("response.html", res = x)

if __name__ == "__main__" :
    app.run(debug=True)