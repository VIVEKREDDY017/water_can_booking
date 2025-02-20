from flask import Blueprint, request, jsonify, render_template,session, flash,redirect,url_for
from werkzeug.security import generate_password_hash
from app.models.user import User
from werkzeug.security import check_password_hash
from datetime import datetime
from app import db
import hashlib
# from app.forms import OrderForm,TrackOrderForm
from werkzeug.security import generate_password_hash
from flask import Blueprint, request, jsonify, render_template, session, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User,Order
from sqlalchemy.orm import aliased
from flask_login import login_required


bp = Blueprint('register', __name__)

@bp.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match", 400

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('register.login'))

    return render_template('index.html')

@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['email']=user.email
            flash('Login successful!', 'success')
            return redirect(url_for('register.dashboard'))
            
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('register.login'))

    return render_template('login.html')
@bp.route('/dashboard')
def dashboard():
    if 'username' in session:
        user = {'name': session['username']}  # Construct user object manually
    else:
        user = None
    return render_template('dashboard.html', user=user)



@bp.route("/home")
def home():
    return render_template("home.html")

@bp.route("/settings")
def settings():
    print("Session Data:", session)  # Debugging step
    return render_template("settings.html", username=session.get("username"), email=session.get("email"))


@bp.route("/update-settings", methods=["POST"])
def update_settings():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = db.session.get(User, session["user_id"])
    
    if not user:
        return "User not found", 404

    user.username = request.form.get("username")
    user.email = request.form.get("email")
    user.address=request.form.get("address")

    db.session.commit()  # 🔥 Commit changes

    session["username"] = user.username
    session["email"] = user.email  # Update session data
    session["address"] = user.address

    flash("profile updated successfully!", "success")
    return redirect(url_for("register.settings"))


@bp.route("/logout")
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for("register.login")) 

from flask_login import login_required

@bp.route('/order_history')
def order_history():
    
    if 'user_id' not in session:
        flash("Please log in to view your order history.", "warning")
        return redirect(url_for('book_order'))  # Redirect to order page instead of login

    user_id = session['user_id']
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.order_date.desc()).all()

    return render_template('order_history.html', orders=orders)


WATER_CAN_PRICE = 50.0
@bp.route('/order', methods=['GET', 'POST'])
def book_order():
    if 'user_id' not in session:
        flash("Please log in to place an order.", "danger")
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        quantity = request.form.get('quantity')

        # Validate input
        if not name or not address or not quantity:
            flash("All fields are required!", "danger")
            return redirect(url_for('book_order'))

        try:
            quantity = int(quantity)
            if quantity <= 0:
                flash("Quantity must be a positive number!", "danger")
                return redirect(url_for('book_order'))
        except ValueError:
            flash("Invalid quantity!", "danger")
            return redirect(url_for('book_order'))

        user_id = session['user_id']
        total_price = quantity * WATER_CAN_PRICE

        # Create and save order
        new_order = Order(
            user_id=user_id,
            name=name,
            address=address,
            quantity=quantity,
            total_price=total_price,
            status="Pending",
            order_date=datetime.now()
        )

        db.session.add(new_order)
        db.session.commit()

        flash("Order placed successfully!", "success")
        return redirect(url_for('register.dashboard'))

    return render_template('order.html')


@bp.route('/track_order', methods=['GET', 'POST'])
def track_order():
    order = None  # Default to no order found
    if request.method == 'POST':
        order_id = request.form.get('order_id')

        # Query order from database
        order = Order.query.filter_by(id=order_id).first()

        if not order:
            flash('Order not found. Please check the Order ID.', 'danger')
        else:
            flash(f"Order {order.id} found!", 'success')

    return render_template('order_tracking.html', order=order)