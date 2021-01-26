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
                
def initialize():
    db.connect()
    db.create_tables([Entry], safe=True)
    
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
                
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def menu():
    menu_options = OrderedDict([
    ("V", view_entries),
    ("A", add_entry),
    ("B", backup),])
    
    choice = None
    
    while choice != "Q":
        clear()
        print("Enter 'Q' to quit")
        for key, value in menu_options.items():
            print("{}) {}".format(key, value.__doc__))
        choice = input("Action: ").upper().strip()
        
        if choice in menu_options:
            clear()
            menu_options[choice]()
            
def display(entry):
    timestamp = entry.date_updated.strftime('%m/%d/%Y')
    print("ID: " + str(entry.product_id))
    print("Name: " + entry.product_name)
    print("Price: $" + "{:.2f}".format(entry.product_price / 100))
    print("Quantity: " + str(entry.product_quantity))
    print("Last updated: " + timestamp)
    
           
def view_entries():
    """View all entries"""
    entries = Entry.select().order_by(Entry.product_id.asc())
    selection = (input("Please enter a product ID (leave blank to view all): "))
    if selection == "":
        for entry in entries:
            display(entry)
        input("Press Enter to continue")
    elif selection.isnumeric() and 1 <= int(selection) <= len(entries):
        entry = Entry.get_by_id(int(selection))
        display(entry)
        input("Press Enter to continue")
    else:
        print("That's not a valid Product ID")
        input("Press Enter to continue")

def add_entry():
    """Add a new entry"""
    pass

def backup():
    """Backup the database"""
    pass

if __name__ =="__main__":
    initialize()
    add_items()
    menu()
            
            
            