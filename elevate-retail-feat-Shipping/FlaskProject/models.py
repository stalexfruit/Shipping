import os
if os.getenv("FLASK_ENV") == "pos":
    from src.utils.db_utils import db
else:
    from database import db


class Customer(db.Model):
    __tablename__ = 'customer'

    Customer_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    First_Name = db.Column(db.String(50), nullable=False)
    Last_Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(254), unique=True, nullable=False)
    Phone = db.Column(db.String(20))
    Membership_Level = db.Column(db.String(50), nullable=False)
    Created_At = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    Updated_At = db.Column(db.DateTime, nullable=True, onupdate=db.func.now())
    Deleted_At = db.Column(db.DateTime, nullable=True)

    # Relationships
    orders = db.relationship('Order', back_populates='customer')


# Define the Order model
class Order(db.Model):
    __tablename__ = 'order'

    Order_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Customer_ID = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    Order_Date = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    # Relationships
    customer = db.relationship('Customer', back_populates='orders')
    shipping = db.relationship('Shipping', back_populates='order')


# Define the Shipping model
class Shipping(db.Model):
    __tablename__ = 'shipping'

    Shipping_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Order_ID = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)
    Cost = db.Column(db.Numeric(8, 2), nullable=False)
    Shipped_On = db.Column(db.DateTime, nullable=True)
    Expected_By = db.Column(db.DateTime, nullable=True)
    Status = db.Column(db.String(15), nullable=False)
    Carrier = db.Column(db.String(100), nullable=False)
    Tracking_Number = db.Column(db.String(50), nullable=False)
    Created_At = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    Updated_At = db.Column(db.DateTime, nullable=True, onupdate=db.func.now())
    Shipping_Address_ID = db.Column(db.Integer, nullable=False)
    Billing_Address_ID = db.Column(db.Integer, nullable=False)

    # Relationships
    order = db.relationship('Order', back_populates='shippings')
