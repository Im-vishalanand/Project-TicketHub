from dotenv import dotenv_values
env_vars = dotenv_values('.env')
import os
from flask import Blueprint, Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from model import Admin
from model import User
from flask_bcrypt import Bcrypt
import uuid
import jwt
import mongoengine


app = Flask(__name__)
CORS(app)

bcrypt = Bcrypt(app)


# # MongoDB Atlas connection details
# MONGO_URI = env_vars['MONGO_URI']
# print(MONGO_URI)
# DB_NAME = 'tickethubDB'
# MENU_COLLECTION = 'menu'
# ORDERS_COLLECTION = 'orders'

# # MongoDB client
# client = MongoClient(MONGO_URI)
# db = client[DB_NAME]
# menu_collection = db[MENU_COLLECTION]
# orders_collection = db[ORDERS_COLLECTION]


# Set up the default MongoDB connection
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb+srv://imvishalanand11:HXKXtYsncu4rqNmq@cluster0.kjlyzjl.mongodb.net/tickethubDB?retryWrites=true&w=majority',  
}

mongoengine.connect(host=app.config['MONGODB_SETTINGS']['host'])



# Routes for managing the admin

# admin signup
# http://127.0.0.1:5000/admin/signup
@app.route("/admin/signup", methods=["POST"])
def admin_signup():
    new_admin = request.get_json()

    # Check if the admin_email already exists
    existing_admin = Admin.objects(admin_email=new_admin["admin_email"]).first()
    if existing_admin:
        return jsonify({"message": "admin_Email already exists"}), 400

    # Import bcrypt here to avoid circular import error
    from flask_bcrypt import Bcrypt

    # Encrypt the password using bcrypt
    hashed_password = bcrypt.generate_password_hash(new_admin["admin_password"]).decode(
        "utf-8"
    )

    # Create a new admin
    admin = Admin(
        admin_email=new_admin["admin_email"],
        admin_password=hashed_password,
        admin_name=new_admin["admin_name"],
        is_admin=True,
    )
    admin.save()

    return jsonify({"message": "Signup successful"}), 201



# admin login
# http://127.0.0.1:5000/admin/login
@app.route("/admin/login", methods=["POST"])
def admin_login():
    login_data = request.get_json()

    # Find the admin with the provided email
    admin = Admin.objects(admin_email=login_data["admin_email"], is_admin = True).first()
    if not admin:
        return jsonify({"message": "Wrong Credentials"}), 400

    # Import bcrypt here to avoid circular import error
    from flask_bcrypt import Bcrypt

    # Check if the password is correct
    if bcrypt.check_password_hash(admin.admin_password, login_data["admin_password"]):
        # Generate a token using jsonwebtoken
        token = jwt.encode(
            {"_id": str(admin.id)}, "my signature", algorithm="HS256"
        )

        return jsonify({"message": "Login successful", "token": token}), 200
    else:
        return jsonify({"message": "Wrong password"}), 400



# Routes for managing the user

# get all user
#http://127.0.0.1:5000/
@app.route("/", methods=["GET"])
def get_all_users():
    try:
        all_users = User.objects().to_json()
        print("Database connection is active", all_users)
        return all_users
    except Exception as e:
        print("Database connection is not active",e)
        return "Error: Database connection is not active"
    



# user signup
# http://127.0.0.1:5000/user/signup
@app.route("/user/signup", methods=["POST"])
def user_signup():
    if request.method != "POST" :
        return jsonify({"error message" : "Wrong method for this request"})
    
    new_user = request.get_json()

    # Check if the user_email already exists
    existing_user = User.objects(user_email=new_user["user_email"]).first()
    if existing_user:
        return jsonify({"message": "user_Email already exists"}), 400

    # Import bcrypt here to avoid circular import error
    
    from flask_bcrypt import Bcrypt
    # Encrypt the password using bcrypt
    hashed_password = bcrypt.generate_password_hash(new_user["user_password"]).decode(
        "utf-8"
    )

    # Create a new user
    user = User(
        user_email=new_user["user_email"],
        user_password=hashed_password,
        user_name=new_user["user_name"],
        wallet_balance = 1500,
        bio = new_user["bio"],
        membership_type = new_user["membership_type"],
        gender = new_user["gender"],
        user_status = 'active',
        dob = new_user["dob"],
        movie_show_bookings = [],
        event_show_bookings = []
    )
    user.save()

    return jsonify({"message": "Signup successful"}), 201


# user login
# http://127.0.0.1:5000/user/login
@app.route("/user/login", methods=["POST"])
def user_login() :
    login_data = request.get_json()

    user = User.onjects(user_email = login_data["user_email"]).first()
    if not user :
        return jsonify({"message" : "Wrong Email"}), 400
    
    import bcrypt

    if bcrypt.check_password_hash(user.user_password, login_data["user_password"]):
        token = jwt.encode({"_id" : str(user.id)}, "my signature", algorithm="HS256")
        return jsonify({"message" : "Login successful", "token" : token}), 200
    else :
        return jsonify({"message" : "Wrong password !!"}), 400



# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)


