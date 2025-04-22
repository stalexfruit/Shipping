from flask_sqlalchemy import SQLAlchemy
import sqlite3
#from shipping_app import app
from datetime import datetime

db = SQLAlchemy()

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/shipping_db'

connection = sqlite3.connect('shippingDatabase.db')
cursor = connection.cursor()

# Creating Customer Table
# Creating Customer Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Customer (
    Customer_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    First_Name TEXT NOT NULL,
    Last_Name TEXT NOT NULL,
    Email TEXT NOT NULL UNIQUE,
    Phone TEXT,
    Membership_Level TEXT NOT NULL,
    Created_At DATETIME NOT NULL DEFAULT (datetime('now')),
    Updated_At DATETIME,
    Deleted_At DATETIME
)
''')
# Creating Order Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS [Order] (
    Order_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Customer_ID INTEGER NOT NULL,
    Order_Date DATETIME NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID)
)
''')
# Creating Shipping Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Shipping (
    Shipping_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Order_ID INTEGER NOT NULL,
    Cost REAL NOT NULL CHECK (Cost >= 0),
    Shipped_On DATETIME,
    Expected_By DATETIME,
    Ship_Status TEXT NOT NULL CHECK (Ship_Status IN ('Pending', 'Shipped', 'Delivered', 'Returned')),
    Carrier TEXT NOT NULL,
    Tracking_Number TEXT NOT NULL,
    Created_At DATETIME NOT NULL DEFAULT (datetime('now')),
    Updated_At DATETIME,
    Shipping_Address_ID INTEGER NOT NULL,
    Billing_Address_ID INTEGER NOT NULL,
    FOREIGN KEY (Order_ID) REFERENCES [Order](Order_ID)
)
''')

connection.commit()
connection.close()
