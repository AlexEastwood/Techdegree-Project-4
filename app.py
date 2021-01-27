import csv
import datetime
import os
import re
import sys
from collections import OrderedDict

from peewee import *

db = SqliteDatabase("inventory.db")


class Product(Model):
    product_id = AutoField()
    product_name = CharField(unique=True)
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateField(default=datetime.datetime.now)

    class Meta:
        database = db


def initialize():
    db.connect()
    db.create_tables([Product], safe=True)
    db.close()


def add_items():
    with open("inventory.csv", newline="") as csvfile:
        invreader = csv.DictReader(csvfile, delimiter=",")
        items = list(invreader)
        for item in items:
            item["product_quantity"] = int(item["product_quantity"])
            item["product_price"] = int(float(item["product_price"][1:]) * 100)
            item["date_updated"] = (
                datetime.datetime.strptime(item['date_updated'], '%m/%d/%Y').date())
            try:
                Product.create(
                product_name = item['product_name'],
                product_price = item['product_price'],
                product_quantity = item['product_quantity'],
                date_updated = item['date_updated'],
                ).save()
            except IntegrityError:
                item_update = Product.get(product_name = item['product_name'])
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
    ("A", add_product),
    ("B", backup),])

    choice = None
    
    while choice != "Q":
        clear()
        print("Enter 'Q' to quit")
        for key, value in menu_options.items():
            print("{}) {}".format(key, value.__doc__))
        choice = input("Action: ").upper().strip()
        
        if choice == "Q":
            continue
        elif choice in menu_options:
            clear()
            menu_options[choice]()
        else:
            print("That's not a valid option")
            input("Press Enter to continue")

def display(product):
    timestamp = product.date_updated.strftime('%m/%d/%Y')
    print("ID: " + str(product.product_id))
    print("Name: " + product.product_name)
    print("Price: $" + "{:.2f}".format(product.product_price / 100))
    print("Quantity: " + str(product.product_quantity))
    print("Last updated: " + timestamp + "\n")

def view_entries():
    """View all entries"""
    entries = Product.select().order_by(Product.product_id.asc())
    selection = (input("Please enter a product ID (leave blank to view all): "))
    if selection == "":
        for product in entries:
            display(product)
        input("Press Enter to continue")
    elif selection.isnumeric() and 1 <= int(selection) <= len(entries):
        product = Product.get_by_id(int(selection))
        display(product)
        input("Press Enter to continue")
    else:
        print("That's not a valid Product ID")
        input("Press Enter to continue")

def add_product():
    """Add a new product"""
    print("Enter your product.")
    new_name = input("Product Name: ")
    while True:
        try:
            new_quantity = int(input("Quantity: "))
        except ValueError:
            continue
        break
    while True:
        new_price = input("Price ($x.xx): ")
        if re.match(r"\$[0-9]+\.[0-9]{2}", new_price):
            break
        else:
            continue
    
    if input("Save product? [Y/N] ").lower() != "n":
        try:
            Product.create(
            product_name = new_name,
            product_quantity = new_quantity,
            product_price = int(float(new_price[1:]) * 100),
            date_updated = datetime.datetime.now().date()
            ).save()
        except IntegrityError:
            update = Product.get(product_name = new_name)
            update.product_price = int(float(new_price[1:]) * 100)
            update.product_quantity = new_quantity
            update.date_updated = datetime.datetime.now().date()
            update.save()
            
        print("Saved Successfully!")
        input("Press Enter to continue")

def backup():
    """Backup the database"""
    entries = Product.select().order_by(Product.product_id.asc())
    with open("backup.csv", "w", newline='', encoding='utf-8') as csvfile:
        fieldnames = ["product_id", "product_name", "product_quantity", "product_price", "date_updated"]
        backup_writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        
        backup_writer.writeheader()
        for product in entries:
            timestamp = product.date_updated.strftime('%m/%d/%Y')
            backup_writer.writerow({
                "product_id": product.product_id,
                "product_name": product.product_name,
                "product_quantity": product.product_quantity,
                "product_price": product.product_price,
                "date_updated": timestamp
            })

if __name__ =="__main__":
    initialize()
    add_items()
    menu()
