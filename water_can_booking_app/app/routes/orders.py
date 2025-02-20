# from flask import Blueprint, request, jsonify
# from app import db
# from app.models.user import Order, Product, User
# from datetime import datetime
# bp = Blueprint('orders', __name__)

# @bp.route('/orders', methods=['POST'])
# def create_order():
#     try:
#         data = request.get_json()  # Get the data from the POST request

#         # Extract the data from the request body
#         user_id = data.get('user_id')
#         product_id = data.get('product_id')
#         quantity = data.get('quantity')

#         # Check if the required fields are provided
#         if not user_id or not product_id or not quantity:
#             return jsonify({"message": "Missing required fields"}), 400

#         # Check if the user and product exist
#         user = User.query.get(user_id)
#         product = Product.query.get(product_id)

#         if not user:
#             return jsonify({"message": "User not found"}), 404
#         if not product:
#             return jsonify({"message": "Product not found"}), 404

#         # Create a new Order
#         order = Order(
#             user_id=user_id,
#             product_id=product_id,
#             quantity=quantity,
#             order_date=datetime.utcnow()  # Use datetime here
#         )

#         # Add to the session and commit to save to the database
#         db.session.add(order)
#         db.session.commit()

#         # Return a success response
#         return jsonify({
#             "message": "Order created successfully",
#             "order_id": order.id,
#             "user_id": order.user_id,
#             "product_id": order.product_id,
#             "quantity": order.quantity,
#             "order_date": order.order_date.isoformat()
#         }), 201

#     except Exception as e:
#         return jsonify({"message": str(e)}), 500

# @bp.route('/pag_orders', methods=['GET'])
# def get_orders():
#     try:
#         # Get any query parameters for filtering (optional)
#         user_id = request.args.get('user_id')  # Optional filter by user
#         product_id = request.args.get('product_id')  # Optional filter by product
        
#         # Build the query to fetch orders
#         query = Order.query
        
#         if user_id:
#             query = query.filter(Order.user_id == user_id)
        
#         if product_id:
#             query = query.filter(Order.product_id == product_id)
        
#         # Fetch the orders from the database
#         orders = query.all()

#         if not orders:
#             return jsonify({"message": "No orders found"}), 404

#         # Serialize orders data
#         orders_data = []
#         for order in orders:
#             user = User.query.get(order.user_id)
#             product = Product.query.get(order.product_id)

#             order_data = {
#                 "order_id": order.id,
#                 "user_id": order.user_id,
#                 "username": user.username if user else "Unknown",  # Get username from User model
#                 "product_id": order.product_id,
#                 "product_name": product.name if product else "Unknown",  # Get product name from Product model
#                 "quantity": order.quantity,
#                 "order_date": order.order_date.isoformat()
#             }
#             orders_data.append(order_data)

#         return jsonify({"orders": orders_data}), 200

#     except Exception as e:
#         return jsonify({"message": str(e)}), 500