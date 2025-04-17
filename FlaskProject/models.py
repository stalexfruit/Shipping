import os
if os.getenv("FLASK_ENV") == "pos":
    from src.utils.db_utils import db
else:
    from database import db

class Customer(db.Model):
    __tablename__ = 'Customer'
    Customer_ID = db.Column(db.Integer, primary_key=True)  # Primary key
    First_name = db.Column(db.String(255), nullable=False)
    Last_name = db.Column(db.String(255), nullable=False)  # Fixed capitalization for consistency
    Address = db.Column(db.String(255), nullable=False)
    Birthday = db.Column(db.String(10))  # Optional field
    Membership_Level = db.Column(db.String(50))  # Presumed type or classification of customer

    # Relationship to 'Order' class
    orders = db.relationship('Order', backref='customer', lazy=True)


class Order(db.Model):
    __tablename__ = 'Order'
    Order_ID = db.Column(db.Integer, primary_key=True)  # Primary key
    Customer_ID = db.Column(db.Integer, db.ForeignKey('Customer.Customer_ID'), nullable=False)  # Foreign key linking to 'Customer'
    Membership_Level = db.Column(db.String(50), nullable=False)  # Changed from Float to String to reflect appropriate data
    Shipping_Option = db.Column(db.String(50), nullable=False)
    Shipping_Cost = db.Column(db.Float, nullable=False)

    # Relationship to 'Shipping' class
    shipping = db.relationship('Shipping', backref='order', lazy=True)


class Shipping(db.Model):
    __tablename__ = 'Shipping'
    Shipping_ID = db.Column(db.Integer, primary_key=True)  # Primary key
    Order_ID = db.Column(db.Integer, db.ForeignKey('Order.Order_ID'), nullable=False)  # Foreign key linking to 'Order'
    Address = db.Column(db.String(255), nullable=False)
    City = db.Column(db.String(100))
    Zip_Code = db.Column(db.String(20))
    State = db.Column(db.String(50))

class Tracking(db.Model):
    __tablename__ = 'Tracking'
    Tracking_ID = db.Column(db.Integer, primary_key=True)
    Order_ID = db.Column(db.Integer, db.ForeignKey('Order.Order_ID'), nullable=False)
    TrackingNumber = db.Column(db.String(255))
    CurrentLocation = db.Column(db.String(255))
    ExpectedDeliveryDate = db.Column(db.Date)