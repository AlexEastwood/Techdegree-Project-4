import csv
import datetime
import os
import sys
from collections import OrderedDict

from peewee import *

db = SqliteDatabase("inventory.db")

class Entry(Model):
    product_id = CharField(primary_key=True)
    product_name = CharField()
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateField(default=datetime.datetime.now)

    class Meta:
        database = db
        
def initialize():
    db.connect()
    db.create_tables([Entry], safe=True)
    
if __name__ =="__main__":
    initialize()
    
    with open("inventory.csv", newline = "") as csvfile:
        invreader = csv.DictReader(csvfile, delimiter = ",")
        rows = list(invreader)
        for row in rows[1:]:
            row["product_quantity"] = int(row["product_quantity"])
            row["product_price"] = int(float(row["product_price"][1:]) * 100)
            row["date_updated"] = datetime.datetime.strptime(row["date_updated"], "%m/%d/%Y")
        
        print(rows)
            
            
            