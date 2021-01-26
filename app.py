import csv
import datetime
import os
import sys
from collections import OrderedDict

from peewee import *

db = SqliteDatabase("inventory.db")

class Entry(Model):
    product_id = AutoField()
    product_name = CharField(unique=True)
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateField(default=datetime.datetime.now)

    class Meta:
        database = db
        
def add_items():     
    with open("inventory.csv", newline = "") as csvfile:
        invreader = csv.DictReader(csvfile, delimiter = ",")
        items = list(invreader)
        for item in items:
            item["product_quantity"] = int(item["product_quantity"])
            item["product_price"] = int(float(item["product_price"][1:]) * 100)
            item["date_updated"] = (datetime.datetime.strptime(item['date_updated'],'%m/%d/%Y').date())
            try:
                Entry.create(
                product_name = item['product_name'],
                product_price = item['product_price'],
                product_quantity = item['product_quantity'],
                date_updated = item['date_updated'],
                ).save()
            except IntegrityError:
                item_update = Entry.get(product_name = item['product_name'])
                item_update.product_name = item['product_name']
                item_update.product_price = item['product_price']
                item_update.product_quantity = item['product_quantity']
                item_update.date_updated = item['date_updated']
                item_update.save()
                
def initialize():
    db.connect()
    db.create_tables([Entry], safe=True)
  
if __name__ =="__main__":
    initialize()
    add_items()
            
            
            