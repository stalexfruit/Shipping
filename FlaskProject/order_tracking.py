import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from FlaskProject.shipping_app import app
if os.getenv("FLASK_ENV") == "pos":
    from src.utils.db_utils import db
else:
    from database import db

db = SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/shipping_db'

connection = sqlite3.connect('shippingDatabase.db')
cursor = connection.cursor()


#
def orderTracking(orderID, orderCase):
    match orderCase:

        case "processing":
            cursor.execute('''
            UPDATE Shipping
            SET Ship_Status = ?, Updated_At = ?
            WHERE Order_ID = ?
            ''', ("Processing Order", datetime.now(), orderID))
            return "Successful!"

        case "warehouse1":
            cursor.execute('''
            UPDATE Shipping
            SET Ship_Status = ?, Updated_At = ?
            WHERE Order_ID = ?
            ''', ("In Warehouse 1", datetime.now(), orderID))
            return "Successful!"

        case "warehouse1-delivering":
            cursor.execute('''
            UPDATE Shipping
            SET Ship_Status = ?, Updated_At = ?
            WHERE Order_ID = ?
            ''', ("En Route to Warehouse 1", datetime.now(), orderID))
            return "Successful!"

        case "warehouse2":
            cursor.execute('''
            UPDATE Shipping
            SET Ship_Status = ?, Updated_At = ?
            WHERE Order_ID = ?
            ''', ("In Warehouse 2", datetime.now(), orderID))
            return "Successful!"

        case "warehouse2-delivering":
            cursor.execute('''
            UPDATE Shipping
            SET Ship_Status = ?, Updated_At = ?
            WHERE Order_ID = ?
            ''', ("En Route to Warehouse 2", datetime.now(), orderID))
            return "Successful!"

        case "customerAddress":
            cursor.execute('''
            UPDATE Shipping
            SET Ship_Status = ?, Updated_At = ?
            WHERE Order_ID = ?
            ''', ("Delivered to Customer", datetime.now(), orderID))
            return "Successful!"

        case "customerAddress-delivering":
            cursor.execute('''
            UPDATE Shipping
            SET Ship_Status = ?, Updated_At = ?
            WHERE Order_ID = ?
            ''', ("En Route to Customer", datetime.now(), orderID))
            return "Successful!"

        case _:
            return "ERROR: INVALID COMMAND SENT"