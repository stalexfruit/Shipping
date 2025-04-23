import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from FlaskProject.shipping_app import app
if os.getenv("FLASK_ENV") == "pos":
    from src.utils.db_utils import db
    from src.models import Shipping
else:
    from database import db

db = SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/shipping_db'

connection = sqlite3.connect('shippingDatabase.db')
cursor = connection.cursor()

if os.getenv("FLASK_ENV") != "pos":
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
else:
    def order_tracking(order_id: int, order_case: str) -> str:
        """Update the Shipping.ship_status and Shipping.updated_at for a given order."""
        # lookup the existing Shipping row
        shipping = Shipping.query.filter_by(Order_ID=order_id).first()
        if shipping is None:
            return "ERROR: ORDER NOT FOUND"

        # map incoming cases to the human-readable status
        status_map = {
            "pending":   "Pending",
            "shipped":   "Shipped",
            "delivered": "Delivered",
        }
        new_status = status_map.get(order_case.lower())
        if not new_status:
            return "ERROR: INVALID COMMAND SENT"

        # apply and commit
        shipping.ship_status = new_status
        shipping.updated_at  = datetime.utcnow()
        db.session.commit()

        return "Successful!"