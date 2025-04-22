import os
from flask import Blueprint, request, jsonify

# Environment-specific import handling
if os.getenv("FLASK_ENV") == "pos":
    from src.utils.db_utils import db
else:
    from database import db

from .models import Customer, Order

# Define the shipping blueprint
shipping_bp = Blueprint('shipping', __name__)


def calculate_shipping_cost(customer_type, shipping_option):
    """
    Calculate the shipping cost based on customer type and shipping option.

    :param customer_type: Type of the customer (e.g., 'Prime', 'Regular').
    :param shipping_option: Chosen shipping option (e.g., 'FedEx', 'UPS').
    :return: Calculated shipping cost, or 0.0 for Prime members.
    """
    shipping_rates = {"Fedex": 10.0, "UPS": 8.0, "Amazon": 8.0, "USPS": 6.0}
    return 0.0 if customer_type.lower() == "prime" else shipping_rates.get(Shipping.Carrier, 0.0)


@shipping_bp.route('/orders', methods=['POST'])
def create_order():
    """
    Flask route to create a new order.

    :return: A success message with shipping cost, or an error response.
    """
    data = request.get_json()

    # Validate required fields
    required_fields = ['Customer_ID','Membership_Level','Shipping_Company', 'Shipping_Option']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Validate and fetch customer from the database
    customer = Customer.query.get(data['Customer_ID'])
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    company = Shipping.Carrier.query.filler_by(Name=data['Shipping_Company']).first()

    # Calculate shipping cost
    Cost = calculate_shipping_cost(customer.Type, data['Shipping_Option'])

    # Create new order
    new_order = Order(
        Customer_ID=data['Customer_ID'],
        Membership_Level=data['Membership_Level'],
        Shipping_ID=company.Company_ID,
        Carrier=data['Shipping_Option'],
        Cost=Shipping.Cost

    )

    # Add to session and commit
    db.session.add(new_order)
    db.session.commit()

    # Respond with success message
    return jsonify({
        "message": "Order created successfully.",
        "Shipping_Cost": Shipping.Cost,
        "Shipping_Company": Shipping.Carrier
    }), 201

