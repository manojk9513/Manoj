from pymongo import MongoClient
import csv
import os

# read csv file as a list of lists
client = MongoClient('localhost', 27017)
db = client["stocks"]

yourfile = os.listdir("C:/Users/hp/PycharmProjects/stock_dashboard/stocks/")
for name in yourfile:
    k = name.rfind(".")
    col = db[name[:k]]
    print(name)
    with open('C:/Users/hp/PycharmProjects/stock_dashboard/stocks/'+name, 'r') as read_obj:
        csv_reader = csv.DictReader(read_obj)
        mylist = list(csv_reader)
        x = col.insert_many(mylist)
        print(x.inserted_ids)