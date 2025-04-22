from flask_sqlalchemy import SQLAlchemy
import sqlite3
from FlaskProject.shipping_app import app

db = SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/shipping_db'

connection = sqlite3.connect('shippingDatabase.db')
cursor = connection.cursor()

# Creating Customer Table
cursor.execute('''
CREATE TABLE Customer (
    Customer_ID INT IDENTITY(1,1) PRIMARY KEY,
    First_Name VARCHAR(50) NOT NULL,
    Last_Name VARCHAR(50) NOT NULL,
    Email VARCHAR(254) NOT NULL UNIQUE,
    Phone VARCHAR(20),
    Membership_Level VARCHAR(50) NOT NULL,
    Created_At DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    Updated_At DATETIME2 NULL,
    Deleted_At DATETIME2 NULL,
    CONSTRAINT FK_Customer_Member FOREIGN KEY (Membership_Level)
        REFERENCES Member(Membership_Level)
)''')

# Creating Order Table
cursor.execute('''
CREATE TABLE [Order] (
    Order_ID INT IDENTITY(1,1) PRIMARY KEY,
    Customer_ID INT NOT NULL,
    Order_Date DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CONSTRAINT FK_Order_Customer FOREIGN KEY (Customer_ID)
        REFERENCES Customer(Customer_ID)
)''')

# Create Shipping Table
cursor.execute('''
CREATE TABLE Shipping (
    Shipping_ID INT IDENTITY(1,1) PRIMARY KEY,
    Order_ID INT NOT NULL,
    Cost DECIMAL(8,2) NOT NULL CHECK (Cost >= 0),
    Shipped_On DATETIME2 NULL,
    Expected_By DATETIME2 NULL,
    Ship_Status VARCHAR(15) NOT NULL CHECK (Ship_Status IN ('Pending', 'Shipped', 'Delivered', 'Returned')),
    Carrier VARCHAR(100) NOT NULL,
    Tracking_Number VARCHAR(50) NOT NULL,
    Created_At DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    Updated_At DATETIME2 NULL,
    Shipping_Address_ID INT NOT NULL,
    Billing_Address_ID INT NOT NULL,
    CONSTRAINT FK_Shipping_Order FOREIGN KEY (Order_ID)
        REFERENCES [Order](Order_ID),
    CONSTRAINT FK_Shipping_Address FOREIGN KEY (Shipping_Address_ID)
        REFERENCES Customer_Address(Address_ID),
    CONSTRAINT FK_Billing_Address FOREIGN KEY (Billing_Address_ID)
        REFERENCES Customer_Address(Address_ID)
)''')

connection.commit()
connection.close()
