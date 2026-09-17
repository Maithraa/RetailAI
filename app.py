from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime
import smtplib
import os
from email.message import EmailMessage


app = Flask(__name__)

app.secret_key = "retailai_secret_key"


# ============================================================
# EMAIL CONFIGURATION
# ============================================================

SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")


def send_email(receiver_email, subject, body):

    try:

        msg = EmailMessage()

        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email
        msg["Subject"] = subject

        msg.set_content(body)

        # Gmail SMTP SSL
        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as server:

            server.login(
                SENDER_EMAIL,
                GMAIL_APP_PASSWORD
            )

            server.send_message(msg)

        print("✅ Email sent successfully to:", receiver_email)

        return True

    except Exception as e:

        print("❌ Email sending failed!")
        print("ERROR:", e)

        return False


# ============================================================
# DATABASE
# ============================================================

def get_db():

    conn = sqlite3.connect("retailai.db")

    conn.row_factory = sqlite3.Row

    return conn


def create_table():

    conn = get_db()

    # --------------------------------------------------------
    # USERS TABLE
    # --------------------------------------------------------

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL
        )
    """)

    # --------------------------------------------------------
    # ORDERS TABLE
    # --------------------------------------------------------

    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            customer_name TEXT,

            phone TEXT,

            address TEXT,

            payment_method TEXT,

            items TEXT,

            total REAL,

            order_date TEXT
        )
    """)

    conn.commit()

    conn.close()


create_table()


# ============================================================
# PRODUCT DATA
# ============================================================

# IMPORTANT:
# Keep your COMPLETE existing products dictionary here.
# Your existing fruits, vegetables, chocolates, drinks,
# snacks and household data can remain exactly the same.

products = {

    "fruits": [

        {
            "name": "Fresh Apple",
            "price": 120,
            "emoji": "🍎",
            "image": "https://images.pexels.com/photos/102104/pexels-photo-102104.jpeg"
        },

        {
            "name": "Fresh Banana",
            "price": 60,
            "emoji": "🍌",
            "image": "https://images.pexels.com/photos/1093038/pexels-photo-1093038.jpeg"
        },

        {
            "name": "Fresh Orange",
            "price": 80,
            "emoji": "🍊",
            "image": "https://images.pexels.com/photos/161559/background-orange-fruit-orange-161559.jpeg"
        },

        {
            "name": "Fresh Grapes",
            "price": 100,
            "emoji": "🍇",
            "image": "https://images.pexels.com/photos/708777/pexels-photo-708777.jpeg"
        },

        {
            "name": "Fresh Mango",
            "price": 90,
            "emoji": "🥭",
            "image": "https://images.pexels.com/photos/2294471/pexels-photo-2294471.jpeg"
        },

        {
            "name": "Fresh Watermelon",
            "price": 70,
            "emoji": "🍉",
            "image": "https://images.pexels.com/photos/1313267/pexels-photo-1313267.jpeg"
        },

        {
            "name": "Fresh Pineapple",
            "price": 110,
            "emoji": "🍍",
            "image": "https://images.pexels.com/photos/947879/pexels-photo-947879.jpeg"
        },

        {
            "name": "Fresh Strawberry",
            "price": 150,
            "emoji": "🍓",
            "image": "https://images.pexels.com/photos/46174/strawberries-berries-fruit-freshness-46174.jpeg"
        },

        {
            "name": "Fresh Kiwi",
            "price": 130,
            "emoji": "🥝",
            "image": "https://images.pexels.com/photos/734102/pexels-photo-734102.jpeg"
        },

        {
            "name": "Fresh Papaya",
            "price": 85,
            "emoji": "🥭",
            "image": "https://images.pexels.com/photos/594584/pexels-photo-594584.jpeg"
        }
    ],


    "vegetables": [

        {
            "name": "Fresh Carrot",
            "price": 50,
            "emoji": "🥕",
            "image": "https://images.pexels.com/photos/143133/pexels-photo-143133.jpeg"
        },

        {
            "name": "Fresh Potato",
            "price": 40,
            "emoji": "🥔",
            "image": "https://images.pexels.com/photos/144248/potatoes-vegetables-food-fresh-144248.jpeg"
        },

        {
            "name": "Fresh Tomato",
            "price": 40,
            "emoji": "🍅",
            "image": "https://images.pexels.com/photos/533280/pexels-photo-533280.jpeg"
        },

        {
            "name": "Fresh Onion",
            "price": 55,
            "emoji": "🧅",
            "image": "https://images.pexels.com/photos/144206/onion-vegetables-bulb-vegetable-144206.jpeg"
        },

        {
            "name": "Fresh Broccoli",
            "price": 80,
            "emoji": "🥦",
            "image": "https://images.pexels.com/photos/161514/broccoli-vegetable-food-green-161514.jpeg"
        },

        {
            "name": "Fresh Cabbage",
            "price": 45,
            "emoji": "🥬",
            "image": "https://images.pexels.com/photos/257276/pexels-photo-257276.jpeg"
        },

        {
            "name": "Fresh Cauliflower",
            "price": 60,
            "emoji": "🥦",
            "image": "https://images.pexels.com/photos/461208/pexels-photo-461208.jpeg"
        },

        {
            "name": "Fresh Capsicum",
            "price": 70,
            "emoji": "🫑",
            "image": "https://images.pexels.com/photos/128420/pexels-photo-128420.jpeg"
        },

        {
            "name": "Fresh Brinjal",
            "price": 50,
            "emoji": "🍆",
            "image": "https://images.pexels.com/photos/321551/pexels-photo-321551.jpeg"
        },

        {
            "name": "Fresh Cucumber",
            "price": 45,
            "emoji": "🥒",
            "image": "https://images.pexels.com/photos/2329440/pexels-photo-2329440.jpeg"
        }
    ],


    "chocolates": [

        {"name": "Dairy Milk", "price": 50, "emoji": "🍫", "image": "dairy_milk.jpg"},
        {"name": "5 Star", "price": 20, "emoji": "🍫", "image": "5_star.jpg"},
        {"name": "KitKat", "price": 40, "emoji": "🍫", "image": "kitkat.jpg"},
        {"name": "Perk", "price": 20, "emoji": "🍫", "image": "perk.jpg"},
        {"name": "Munch", "price": 20, "emoji": "🍫", "image": "munch.jpg"},
        {"name": "Kinder Joy", "price": 50, "emoji": "🍫", "image": "kinder_joy.jpg"},
        {"name": "Milkybar", "price": 30, "emoji": "🍫", "image": "milkybar.jpg"},
        {"name": "Ferrero Rocher", "price": 120, "emoji": "🍫", "image": "ferrero_rocher.jpg"},
        {"name": "Toblerone", "price": 150, "emoji": "🍫", "image": "toblerone.jpg"},
        {"name": "Hershey's", "price": 100, "emoji": "🍫", "image": "hersheys.jpg"}
    ],


    "drinks": [

        {"name": "Coca Cola", "price": 40, "emoji": "🥤", "image": "coca_cola.jpg"},
        {"name": "Pepsi", "price": 40, "emoji": "🥤", "image": "pepsi.jpg"},
        {"name": "Sprite", "price": 40, "emoji": "🥤", "image": "sprite.jpg"},
        {"name": "Fanta", "price": 40, "emoji": "🥤", "image": "fanta.jpg"},
        {"name": "Maaza", "price": 45, "emoji": "🧃", "image": "maaza.jpg"},
        {"name": "Slice", "price": 40, "emoji": "🥭", "image": "slice.jpg"},
        {"name": "Real Fruit Juice", "price": 60, "emoji": "🧃", "image": "real_juice.jpg"},
        {"name": "Paper Boat", "price": 50, "emoji": "🧃", "image": "paper_boat.jpg"},
        {"name": "Red Bull", "price": 125, "emoji": "🥤", "image": "red_bull.jpg"},
        {"name": "Appy Fizz", "price": 40, "emoji": "🥤", "image": "appy_fizz.jpg"}
    ],


    "snacks": [

        {"name": "Lays Classic", "price": 20, "emoji": "🥔", "image": "lays_classic.jpg"},
        {"name": "Kurkure", "price": 20, "emoji": "🥨", "image": "kurkure.jpg"},
        {"name": "Bingo Mad Angles", "price": 20, "emoji": "🥨", "image": "bingo.jpg"},
        {"name": "Unibic Cookies", "price": 40, "emoji": "🍪", "image": "unibic.jpg"},
        {"name": "Parle-G Biscuits", "price": 10, "emoji": "🍪", "image": "parle_g.jpg"},
        {"name": "Good Day", "price": 30, "emoji": "🍪", "image": "good_day.jpg"},
        {"name": "Haldiram's Bhujia", "price": 50, "emoji": "🥨", "image": "bhujia.jpg"},
        {"name": "Popcorn", "price": 30, "emoji": "🍿", "image": "popcorn.jpg"},
        {"name": "Too Yumm Chips", "price": 30, "emoji": "🥔", "image": "too_yumm.jpg"},
        {"name": "Uncle Chipps", "price": 20, "emoji": "🥔", "image": "uncle_chipps.jpg"}
    ],


    "household": [

        {"name": "Vim Dishwash Liquid", "price": 90, "emoji": "🧴", "image": "vim.jpg"},
        {"name": "Harpic Toilet Cleaner", "price": 110, "emoji": "🧴", "image": "harpic.jpg"},
        {"name": "Lizol Floor Cleaner", "price": 120, "emoji": "🧴", "image": "lizol.jpg"},
        {"name": "Surf Excel", "price": 150, "emoji": "🧺", "image": "surf_excel.jpg"},
        {"name": "Colin Glass Cleaner", "price": 100, "emoji": "🧴", "image": "colin.jpg"},
        {"name": "Scotch-Brite Scrub Pad", "price": 40, "emoji": "🧽", "image": "scotch_brite.jpg"},
        {"name": "Dettol Liquid", "price": 90, "emoji": "🧴", "image": "dettol.jpg"},
        {"name": "Tissue Paper", "price": 60, "emoji": "🧻", "image": "tissue.jpg"},
        {"name": "Cleaning Brush", "price": 70, "emoji": "🧹", "image": "cleaning_brush.jpg"},
        {"name": "Garbage Bags", "price": 80, "emoji": "🗑️", "image": "garbage_bags.jpg"}
    ]
}


# ============================================================
# CART COUNT
# ============================================================

@app.context_processor
def inject_cart_count():

    cart = session.get("cart", [])

    cart_count = sum(
        item.get("quantity", 1)
        for item in cart
    )

    return {
        "cart_count": cart_count
    }


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html",
        user_name=session.get("user_name")
    )


# ============================================================
# PRODUCTS
# ============================================================

@app.route("/products")
def product_page():

    return render_template(
        "products.html",
        user_name=session.get("user_name")
    )


# ============================================================
# CATEGORY
# ============================================================

@app.route("/category/<category_name>")
def category(category_name):

    category_products = products.get(
        category_name,
        []
    )

    return render_template(
        "category.html",
        category=category_name,
        products=category_products,
        user_name=session.get("user_name")
    )


# ============================================================
# ADD TO CART
# ============================================================

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():

    name = request.form.get("name")

    if not name:
        name = request.form.get("product_name")

    category_name = request.form.get("category")

    price_value = request.form.get("price")

    emoji = request.form.get(
        "emoji",
        "🛒"
    )

    # Find product price
    if not price_value and category_name:

        category_products = products.get(
            category_name,
            []
        )

        for product in category_products:

            if product["name"] == name:

                price_value = product["price"]

                emoji = product.get(
                    "emoji",
                    "🛒"
                )

                break

    # Validate
    if not name or not price_value:

        return redirect(
            request.referrer or
            url_for("home")
        )

    try:

        price = float(price_value)

    except ValueError:

        return redirect(
            request.referrer or
            url_for("home")
        )

    # Get cart
    cart = session.get(
        "cart",
        []
    )

    found = False

    # Existing product
    for item in cart:

        if item["name"] == name:

            item["quantity"] += 1

            found = True

            break

    # New product
    if not found:

        cart.append({

            "name": name,

            "price": price,

            "emoji": emoji,

            "quantity": 1
        })

    session["cart"] = cart

    session.modified = True

    return redirect(
        request.referrer or
        url_for("home")
    )


# ============================================================
# CART
# ============================================================

@app.route("/cart")
def cart():

    cart_items = session.get(
        "cart",
        []
    )

    total = sum(

        item["price"] *
        item["quantity"]

        for item in cart_items
    )

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total,
        user_name=session.get("user_name")
    )


# ============================================================
# INCREASE
# ============================================================

@app.route("/increase/<int:index>")
def increase(index):

    cart = session.get(
        "cart",
        []
    )

    if 0 <= index < len(cart):

        cart[index]["quantity"] += 1

    session["cart"] = cart

    session.modified = True

    return redirect(
        url_for("cart")
    )


# ============================================================
# DECREASE
# ============================================================

@app.route("/decrease/<int:index>")
def decrease(index):

    cart = session.get(
        "cart",
        []
    )

    if 0 <= index < len(cart):

        cart[index]["quantity"] -= 1

        if cart[index]["quantity"] <= 0:

            cart.pop(index)

    session["cart"] = cart

    session.modified = True

    return redirect(
        url_for("cart")
    )


# ============================================================
# REMOVE
# ============================================================

@app.route("/remove/<int:index>")
def remove(index):

    cart = session.get(
        "cart",
        []
    )

    if 0 <= index < len(cart):

        cart.pop(index)

    session["cart"] = cart

    session.modified = True

    return redirect(
        url_for("cart")
    )


# ============================================================
# CLEAR CART
# ============================================================

@app.route("/clear_cart")
def clear_cart():

    session["cart"] = []

    session.modified = True

    return redirect(
        url_for("cart")
    )


# ============================================================
# LOGIN / SIGNUP
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        action = request.form.get(
            "action"
        )

        # ====================================================
        # SIGN UP
        # ====================================================

        if action == "signup":

            name = request.form["name"].strip()

            email = request.form["email"].strip()

            password = request.form["password"]

            conn = get_db()

            try:

                conn.execute(
                    """
                    INSERT INTO users
                    (name, email, password)
                    VALUES (?, ?, ?)
                    """,
                    (
                        name,
                        email,
                        password
                    )
                )

                conn.commit()

                conn.close()

                message = (
                    "Account created successfully! "
                    "Please login."
                )

            except sqlite3.IntegrityError:

                conn.close()

                message = (
                    "Email already registered!"
                )

        # ====================================================
        # LOGIN
        # ====================================================

        elif action == "login":

            email = request.form["email"].strip()

            password = request.form["password"]

            conn = get_db()

            user = conn.execute(
                """
                SELECT *
                FROM users
                WHERE email = ?
                AND password = ?
                """,
                (
                    email,
                    password
                )
            ).fetchone()

            conn.close()

            # =================================================
            # LOGIN SUCCESS
            # =================================================

           if user:

    # Save login session
    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    session["user_email"] = user["email"]

    return redirect(url_for("dashboard"))

                # =================================================
                # IMPORTANT CHANGE
                # LOGIN → DASHBOARD
                # =================================================

                return redirect(
                    url_for("dashboard")
                )

            # =================================================
            # LOGIN FAILED
            # =================================================

            else:

                message = (
                    "Invalid email or password!"
                )

    return render_template(

        "login.html",

        message=message,

        user_name=session.get(
            "user_name"
        )
    )


# ============================================================
# USER DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    # --------------------------------------------------------
    # User must be logged in
    # --------------------------------------------------------

    if not session.get("user_id"):

        return redirect(
            url_for("login")
        )

    user_id = session.get(
        "user_id"
    )

    conn = get_db()

    # --------------------------------------------------------
    # Get user
    # --------------------------------------------------------

    user = conn.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    # --------------------------------------------------------
    # Get all user orders
    # --------------------------------------------------------

    order_list = conn.execute(
        """
        SELECT *
        FROM orders
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,)
    ).fetchall()

    conn.close()

    # --------------------------------------------------------
    # Total Orders
    # --------------------------------------------------------

    total_orders = len(order_list)

    # --------------------------------------------------------
    # Total Spent
    # --------------------------------------------------------

    total_spent = sum(
        float(order["total"] or 0)
        for order in order_list
    )

    # --------------------------------------------------------
    # Recent Order
    # --------------------------------------------------------

    if order_list:

        recent_order = order_list[0]["id"]

    else:

        recent_order = "—"

    # --------------------------------------------------------
    # Send only recent 5 orders to dashboard
    # --------------------------------------------------------

    recent_orders = order_list[:5]

    # --------------------------------------------------------
    # Dashboard
    # --------------------------------------------------------

    return render_template(

        "dashboard.html",

        user=user,

        orders=recent_orders,

        total_orders=total_orders,

        recent_order=recent_order,

        total_spent=f"{total_spent:.2f}",

        user_name=session.get(
            "user_name"
        )
    )

# ============================================================
# USER PROFILE
# ============================================================

@app.route("/profile")
def profile():

    # User must be logged in
    if not session.get("user_id"):

        return redirect(
            url_for("login")
        )

    user_id = session.get(
        "user_id"
    )

    conn = get_db()

    # Get logged-in user details
    user = conn.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    # Get user's orders
    order_list = conn.execute(
        """
        SELECT *
        FROM orders
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,)
    ).fetchall()

    conn.close()

    # If user doesn't exist
    if not user:

        session.clear()

        return redirect(
            url_for("login")
        )

    # Calculate total spent
    total_spent = sum(
        float(order["total"] or 0)
        for order in order_list
    )

    return render_template(
        "profile.html",
        user=user,
        orders=order_list,
        total_orders=len(order_list),
        total_spent=f"{total_spent:.2f}",
        user_name=session.get(
            "user_name"
        )
    )
# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("home")
    )


# ============================================================
# CHECKOUT
# ============================================================

@app.route("/checkout")
def checkout():

    # User must login
    if not session.get("user_id"):

        return redirect(
            url_for("login")
        )

    cart_items = session.get(
        "cart",
        []
    )

    # Empty cart
    if not cart_items:

        return redirect(
            url_for("cart")
        )

    total = sum(

        item["price"] *
        item["quantity"]

        for item in cart_items
    )

    return render_template(

        "checkout.html",

        cart_items=cart_items,

        total=total,

        user_name=session.get(
            "user_name"
        )
    )


# ============================================================
# PLACE ORDER
# ============================================================

@app.route("/place_order", methods=["POST"])
def place_order():

    # --------------------------------------------------------
    # Check login
    # --------------------------------------------------------

    if not session.get("user_id"):

        return redirect(
            url_for("login")
        )

    # --------------------------------------------------------
    # Get cart
    # --------------------------------------------------------

    cart_items = session.get(
        "cart",
        []
    )

    if not cart_items:

        return redirect(
            url_for("cart")
        )

    # --------------------------------------------------------
    # Customer details
    # --------------------------------------------------------

    customer_name = request.form.get(
        "name",
        ""
    ).strip()

    phone = request.form.get(
        "phone",
        ""
    ).strip()

    address = request.form.get(
        "address",
        ""
    ).strip()

    payment_method = request.form.get(
        "payment_method",
        "Cash on Delivery"
    )

    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    if (
        not customer_name
        or not phone
        or not address
    ):

        return """
        <h2>❌ Please fill all delivery details.</h2>

        <a href="/checkout">
            Go Back to Checkout
        </a>
        """

    # --------------------------------------------------------
    # Calculate total
    # --------------------------------------------------------

    total = sum(

        item["price"] *
        item["quantity"]

        for item in cart_items
    )

    # --------------------------------------------------------
    # Convert items to text
    # --------------------------------------------------------

    items_text = ", ".join(

        f"{item['name']} x {item['quantity']}"

        for item in cart_items
    )

    # --------------------------------------------------------
    # Date and time
    # --------------------------------------------------------

    order_date = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    # --------------------------------------------------------
    # User ID
    # --------------------------------------------------------

    user_id = session.get(
        "user_id"
    )

    # --------------------------------------------------------
    # Save order
    # --------------------------------------------------------

    conn = get_db()

    cursor = conn.execute(

        """
        INSERT INTO orders
        (
            user_id,
            customer_name,
            phone,
            address,
            payment_method,
            items,
            total,
            order_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (
            user_id,
            customer_name,
            phone,
            address,
            payment_method,
            items_text,
            total,
            order_date
        )
    )

    conn.commit()

    order_id = cursor.lastrowid

    conn.close()

    # ========================================================
    # ORDER EMAIL
    # ========================================================

    user_email = session.get(
        "user_email"
    )

    user_name = session.get(
        "user_name",
        customer_name
    )

    if user_email:

        send_email(

            user_email,

            f"RetailAI - Order Confirmed #{order_id}",

            f"""Hello {user_name},

Your order has been successfully placed with RetailAI.

========================================
             ORDER DETAILS
========================================

Order ID        : {order_id}

Customer Name   : {customer_name}

Products:
{items_text}

Total Amount    : ₹{total:.2f}

Payment Method  : {payment_method}

Order Status    : Confirmed

Order Date      : {order_date}

========================================

Delivery Address:
{address}

Phone:
{phone}

Thank you for shopping with RetailAI!

We appreciate your order.

Regards,
RetailAI Team
"""
        )

    # --------------------------------------------------------
    # Clear cart
    # --------------------------------------------------------

    session["cart"] = []

    session.modified = True

    # --------------------------------------------------------
    # Save last order
    # --------------------------------------------------------

    session["last_order_id"] = order_id

    session["last_order_total"] = total

    # --------------------------------------------------------
    # Success page
    # --------------------------------------------------------

    return redirect(
        url_for("order_success")
    )


# ============================================================
# ORDER SUCCESS
# ============================================================

@app.route("/order_success")
def order_success():

    order_id = session.get(
        "last_order_id"
    )

    total = session.get(
        "last_order_total",
        0
    )

    if not order_id:

        return redirect(
            url_for("home")
        )

    return render_template(

        "order_success.html",

        order_id=order_id,

        total=total,

        user_name=session.get(
            "user_name"
        )
    )


# ============================================================
# ORDERS
# ============================================================

@app.route("/orders")
def orders():

    # --------------------------------------------------------
    # User must login
    # --------------------------------------------------------

    if not session.get("user_id"):

        return redirect(
            url_for("login")
        )

    user_id = session.get(
        "user_id"
    )

    conn = get_db()

    order_list = conn.execute(

        """
        SELECT *
        FROM orders
        WHERE user_id = ?
        ORDER BY id DESC
        """,

        (user_id,)
    ).fetchall()

    conn.close()

    return render_template(

        "orders.html",

        orders=order_list,

        user_name=session.get(
            "user_name"
        )
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
