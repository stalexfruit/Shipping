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


# function called when an order's state is changed, updating the database accordingly
def orderTracking(orderID, orderCase):
    match orderCase:

        # order is being processed
        case "pending":
            cursor.execute('''
            UPDATE Shipping
            SET Ship_Status = ?, Updated_At = ?
            WHERE Order_ID = ?
            ''', ("Pending", datetime.now(), orderID))
            connection.commit()
            connection.close()
            return "Successful!"

        # order has been delivered to the customer
        case "delivered":
            cursor.execute('''
            UPDATE Shipping
            SET Ship_Status = ?, Updated_At = ?
            WHERE Order_ID = ?
            ''', ("Delivered", datetime.now(), orderID))
            connection.commit()
            connection.close()
            return "Successful!"

        # order is being delivered to the customer
        case "shipped":
            cursor.execute('''
            UPDATE Shipping
            SET Ship_Status = ?, Updated_At = ?
            WHERE Order_ID = ?
            ''', ("Shipped", datetime.now(), orderID))
            connection.commit()
            connection.close()
            return "Successful!"

        # orderCase is something other than the previous cases
        case _:
            return "ERROR: INVALID COMMAND SENT"
