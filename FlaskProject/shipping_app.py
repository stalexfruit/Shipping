'''
Shipping App: This is a backend for the elevate retail capstone project.
Author: Warren Whitcher
'''

# Import required modules
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

# Initialize the Flask app
app = Flask(__name__)

# Database configuration (update credentials for your database)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/shipping_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Customer model
class Customer(db.Model):
    __tablename__ = 'Customer'
    Customer_ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    Address = db.Column(db.String(255), nullable=False)
    Birthday = db.Column(db.String(10))
    Type = db.Column(db.String(50))  # "Prime" for Prime members

# Define the Order model
class Order(db.Model):
    __tablename__ = 'Order'
    Order_ID = db.Column(db.Integer, primary_key=True)
    Customer_ID = db.Column(db.Integer, db.ForeignKey('Customer.Customer_ID'), nullable=False)
    Type = db.Column(db.Float, nullable=False)
    Shipping_Option = db.Column(db.String(50), nullable=False)  # FedEx or UPS
    Shipping_Cost = db.Column(db.Float, nullable=False)

# Define the Product model
class Product(db.Model):
    __tablename__ = 'Product'
    Product_ID = db.Column(db.Integer, primary_key=True)
    Inventory_ID = db.Column(db.Integer)
    Product_name = db.Column(db.String(255), nullable=False)
    Price = db.Column(db.Float, nullable=False)
    Stock = db.Column(db.Integer, nullable=False)

# Define the Shipping model
class Shipping(db.Model):
    __tablename__ = 'Shipping'
    Shipping_ID = db.Column(db.Integer, primary_key=True)
    Address = db.Column(db.String(255), nullable=False)
    City = db.Column(db.String(100))
    Zip_Code = db.Column(db.String(20))
    State = db.Column(db.String(50))

# Calculate shipping cost based on membership and selection
def calculate_shipping_cost(customer_type, shipping_option):
    shipping_rates = {"FedEx": 10.0, "UPS": 8.0}  # Example rates
    return 0.0 if customer_type == "Prime" else shipping_rates.get(shipping_option, 0.0)

# Create a new order with shipping selection
@app.route('/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        customer = Customer.query.get(data['Customer_ID'])
        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        shipping_cost = calculate_shipping_cost(customer.Type, data['Shipping_Option'])
        new_order = Order(
            Customer_ID=data['Customer_ID'],
            Type=data['Type'],
            Shipping_Option=data['Shipping_Option'],
            Shipping_Cost=shipping_cost
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify({"message": "Order created successfully!", "Shipping_Cost": shipping_cost}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Run the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)
