from dotenv import dotenv_values
env_vars = dotenv_values('.env')
from flask import Blueprint, Flask, request, jsonify, Response
from flask_cors import CORS
from pymongo import MongoClient
from model import Admin
from model import User
from model import Movie
from model import Event
from model import Movie_Show
from model import Event_Show
from bson import ObjectId
from werkzeug.routing import BaseConverter
from bson import ObjectId


import json
import os
from flask_bcrypt import Bcrypt
import uuid
import jwt
import mongoengine


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

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


# Custom converter for MongoDB ObjectIDs
class ObjectIdConverter(BaseConverter):
    def to_python(self, value):
        try:
            return ObjectId(value)
        except:
            raise ValueError(f"Not a valid ObjectId: {value}")

    def to_url(self, value):
        if isinstance(value, ObjectId):
            return str(value)
        else:
            raise ValueError(f"Not a valid ObjectId: {value}")



# Register the custom converter with Flask
app.url_map.converters['ObjectId'] = ObjectIdConverter



def calculate_end_time(start_time, duration):
    # Convert start time and duration to minutes
    start_hour, start_minute = map(int, start_time.split(":"))
    duration_hour, duration_minute = map(int, duration.split(":"))
    start_total_minutes = start_hour * 60 + start_minute
    duration_total_minutes = duration_hour * 60 + duration_minute

    # Calculate end time in minutes
    end_total_minutes = start_total_minutes + duration_total_minutes

    # Convert end time from minutes to hours:minutes format
    end_hour = end_total_minutes // 60
    end_minute = end_total_minutes % 60
    end_time = f"{end_hour:02d}:{end_minute:02d}"

    return end_time



def admin_auth_middleware(func):
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            # Verify the token and extract the admin_id
            decoded_token = jwt.decode(token, 'my signature', algorithms=['HS256'])
            admin_id = decoded_token.get('_id')
            # Find the admin with the provided admin_id
            admin = Admin.objects(id=admin_id, is_admin=True).first()
            if not admin:
                return jsonify({"message": "Unauthorized"}), 401
            
            # g.admin_id = admin_id  
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        return func(*args, **kwargs)

    return decorated_function



def user_auth_middleware(func):
    def decorate_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            # Verify the token and extract the user_id
            decoded_token = jwt.decode(token, 'my signature', algorithms=['HS256'])
            user_id = decoded_token.get('_id')
            # Find the user with the provided user_id
            user = User.objects(id=user_id).first()
            if not user:
                return jsonify({"message": "Unauthorized"}), 401
            
            g.user_id = user_id  
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        return func(*args, **kwargs)

    return decorate_function






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




# get all admin
#http://127.0.0.1:5000//admin/all
@app.route("/admin/all", methods=["GET"])
def get_all_admins():
    try:
        all_admins = Admin.objects().to_json()
        print("Database connection is active", all_admins)
        return all_admins
    except Exception as e:
        print("Database connection is not active",e)
        return "Error: Database connection is not active"
    







# Routes for managing the user


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

    user = User.objects(user_email = login_data["user_email"]).first()
    if not user :
        return jsonify({"message" : "Wrong Email"}), 400
    
    from flask_bcrypt import Bcrypt

    if bcrypt.check_password_hash(user.user_password, login_data["user_password"]):
        token = jwt.encode({"_id" : str(user.id)}, "my signature", algorithm="HS256")
        return jsonify({"message" : "Login successful", "token" : token, "username" : user.user_name}), 200
    else :
        return jsonify({"message" : "Wrong password !!"}), 400


# get all user
#http://127.0.0.1:5000/users/all
@app.route("/users/all", methods=["GET"])
def get_all_users():
    try:
        all_users = User.objects().to_json()
        print("Database connection is active", all_users)
        return all_users
    except Exception as e:
        print("Database connection is not active",e)
        return "Error: Database connection is not active"
    

# get a user
#http://127.0.0.1:5000/user/<string:user_id>
@app.route("/user/<string:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    try:
        # Convert the user_id string to a valid ObjectId
        object_id = ObjectId(user_id)

        # Query the User collection by the ObjectId
        user = User.objects.get(id=object_id)

        # Create a dictionary representation of the User object
        user_data = {
            "user_name": user.user_name,
            "user_email": user.user_email,
            "wallet_balance": user.wallet_balance,
            "bio": user.bio,
            "membership_type": user.membership_type,
            "gender": user.gender,
            "user_status": user.user_status,
            "dob": user.dob,
            "movie_show_bookings": [str(show.id) for show in user.movie_show_bookings],
            "event_show_bookings": [str(show.id) for show in user.event_show_bookings],
        }

        # Return the user data as a JSON response
        return jsonify(user_data)

    except User.DoesNotExist:
        # If user is not found, return 404 status code and a message
        return jsonify({"message": "User not found"}), 404

    except Exception as e:
        # Handle any other errors that might occur
        return jsonify({"message": "An error occurred", "error": str(e)}), 500







# Routes for managing the movie


# add movie
# http://127.0.0.1:5000/movie/add
@app.route("/movie/add", methods=["POST"])
def add_movie():
    new_movie = request.get_json()
    movie = Movie(**new_movie)
    movie.save()
    return jsonify({"message": "Movie added successfully"}), 201


# get movies
# http://127.0.0.1:5000/movies/get
@app.route("/movies/get", methods=["GET"])
def get_all_movies():
    all_movies = Movie.objects()
    return all_movies.to_json(), 200




# Routes for managing the event


# add event
# http://127.0.0.1:5000/event/add
@app.route("/event/add", methods=["POST"])
def add_event () :
    new_event = request.get_json()
    event = Event(**new_event)
    event.save()
    return jsonify({"message": "Event added successful"}), 201


# get events
# http://127.0.0.1:5000/events/get
@app.route("/events/get", methods=["GET"])
def get_all_events():
    all_events = Event.objects()
    return all_events.to_json(), 200






# Routes for managing the event_show

# create a new show
# http://127.0.0.1:5000/event_show/create
@app.route("/event_show/create", methods=["POST"])
def create_event_show():
    try:
        new_event_show = request.get_json()
        event_id = new_event_show.get("event_id")

        # Check if event_id is provided in the JSON data
        if not event_id:
            return jsonify({"error": "Event ID is missing"}), 400

        # Check if the event exists in the database
        event = Event.objects(id=event_id).first()
        if not event:
            return jsonify({"error": "Event not found"}), 404

        # Calculate the end time using the helper function
        end_time = calculate_end_time(new_event_show["start_time"], event.duration)

        # Create the Event_Show object and set the end_time field
        event_show = Event_Show(
            event_id=event_id,
            date=new_event_show.get("date"),
            language=new_event_show.get("language"),
            price=new_event_show.get("price"),
            start_time=new_event_show.get("start_time"),
            end_time=end_time,  # Set the calculated end time
            total_seats=new_event_show.get("total_seats", 100),
            booked_seats=new_event_show.get("booked_seats", 0),
            seat_map=new_event_show.get("seat_map", [[0] * 10 for _ in range(10)])  # Default 10x10 seat_map
        )

        event_show.save()

        event.shows.append(event_show.id)
        event.save()

        # Serialize the response data using jsonify
        return jsonify(event_show.to_dict()), 201

    except Exception as e:
        # Handle any unexpected exceptions and return an error response
        return jsonify({"error": str(e)}), 500



# Book a show
# http://127.0.0.1:5000/event_show/<ObjectId:_id>
@app.route("/book_event_show/<ObjectId:_id>", methods=["PUT"])
def book_event_show(_id):
    user_id = g.user_id
    booked_show_data = request.get_json()
    
    # Find the existing Event_Show object by _id
    event_show = Event_Show.objects.with_id(_id)
    # return event_show.to_json()

    if not event_show:
        return jsonify({"message": "Event_Show not found"}), 404
    
    def count_non_zero_values(arr):
        count = 0
        for row in arr:
            for value in row:
                if value != 0:
                    count += 1
        return count

    # Update the fields of the existing Event_Show object with the new data
    for key, value in booked_show_data.items():
        if key == "event_id" or key == "_id" :
            continue
        elif key == "seat_map" :
            setattr(event_show, key, value)
            count = count_non_zero_values(value)
            setattr(event_show, "booked_seats", count)
        else :
            setattr(event_show, key, value)

    event_show.save()

    user = User.objects.with_id(user_id)
    user.event_show_bookings.append(_id)
     # Convert the event_show price to Decimal
    event_show_price = Decimal(str(event_show.price))

    user.wallet_balance = user.wallet_balance - event_show_price
    user.save()

    return event_show.to_json()


# get all the event_shows
# http://127.0.0.1:5000/event_shows
@app.route("/event_shows", methods=["GET"])
def get_all_event_shows():
    event_shows = Event_Show.objects()
    updated_event_shows = []

    for event_show in event_shows:
        # Fetch the corresponding Event object using the event_id attribute of event_show
        event = Event.objects.with_id(event_show.event_id.id)

        if event:
            # Calculate the end time using the helper function
            end_time = calculate_end_time(event_show.start_time, event.duration)

            # Create a new dictionary and copy the fields from event_show and event
            updated_event_show = {
                **event_show.to_mongo(),
                "event_name": event.event_name,
                "end_time": end_time,
                "event_id": str(event.id),  # Convert the ObjectId to a string
            }
            updated_event_shows.append(updated_event_show)

    # Convert the ObjectId to a string for each item in the list
    for show in updated_event_shows:
        show["_id"] = str(show["_id"])

    # Return the Response object with a valid JSON response
    return Response(response=json.dumps(updated_event_shows), status=200, mimetype="application/json")


# get all the event shows related to a particular event
# http://127.0.0.1:5000/event_shows/<ObjectId:_id>
@app.route("/event_shows/<ObjectId:_id>", methods=["GET"])
def get_related_event_shows(_id):
    # Fetch the Event_Show objects related to the specified Event _id
    event_shows = Event_Show.objects(event_id=_id)

    # Fetch the corresponding Event object
    event = Event.objects.with_id(_id)

    if not event:
        return jsonify({"message": "Event not found"}), 404

    # Create a list to store updated Event_Show objects with additional fields
    updated_event_shows = []

    # Update each Event_Show object with end_time and event_name from the Event object
    for event_show in event_shows:
        # Calculate the end time using the helper function
        end_time = calculate_end_time(event_show.start_time, event.duration)

        # Create a new dictionary and copy the fields from event_show and event
        updated_event_show = {
            **event_show.to_mongo(),
            "end_time": end_time,
            "event_name": event.event_name,
            "event_id": str(event.id),  # Convert the ObjectId to a string
        }
        updated_event_shows.append(updated_event_show)

    # Convert the ObjectId to a string for each item in the list
    for show in updated_event_shows:
        show["_id"] = str(show["_id"])

    return jsonify(updated_event_shows)





# Routes for managing the movie_shows



# create a new movie_show
# http://127.0.0.1:5000/movie_show/create
@app.route("/movie_show/create", methods=["POST"])
def create_movie_show():
    new_movie_show = request.get_json()
    movie = Movie.objects(id=new_movie_show["movie_id"]).first()

    # Calculate the end time using the helper function
    end_time = calculate_end_time(new_movie_show["start_time"], movie.duration)

    # Create the Movie_Show object and set the end_time field
    movie_show = Movie_Show(
        movie_id=new_movie_show["movie_id"],
        date=new_movie_show["date"],
        language=new_movie_show["language"],
        price=new_movie_show["price"],
        start_time=new_movie_show["start_time"],
        end_time=end_time,  # Set the calculated end time
        total_seats=new_movie_show.get("total_seats", 100),
        booked_seats=new_movie_show.get("booked_seats", 0),
        seat_map=new_movie_show.get(
            "seat_map", [[0] * 10 for _ in range(10)]
        ),  # Default 10x10 seat_map
    )

    movie_show.save()

    movie.shows.append(movie_show.id)
    movie.save()
    return movie_show.to_json(), 201



# Book a movie_show
# http://127.0.0.1:5000/book_movie_show/<ObjectId:_id>
@app.route("/book_movie_show/<ObjectId:_id>", methods=["PUT"])
def book_movie_show(_id):
    user_id = g.user_id
    booked_show_data = request.get_json()
    
    # Find the existing Movie_Show object by _id
    movie_show = Movie_Show.objects.with_id(_id)
    # return movie_show.to_json()

    if not movie_show:
        return jsonify({"message": "Movie_Show not found"}), 404

    def count_non_zero_values(arr):
        count = 0
        for row in arr:
            for value in row:
                if value != 0:
                    count += 1
        return count
    # Update the fields of the existing Movie_Show object with the new data
    for key, value in booked_show_data.items():
        if key == "movie_id" or key == "_id" :
            continue
        elif key == "seat_map" :
            setattr(movie_show, key, value)
            count = count_non_zero_values(value)
            setattr(movie_show, "booked_seats", count)
        else :
            setattr(movie_show, key, value)

    movie_show.save()

    user = User.objects.with_id(user_id)
    user.movie_show_bookings.append(_id)
     # Convert the movie_show price to Decimal
    movie_show_price = Decimal(str(movie_show.price))

    user.wallet_balance = user.wallet_balance - movie_show_price
    user.save()

    return movie_show.to_json()


# get all the movie_shows
# http://127.0.0.1:5000/movie_shows
@app.route("/movie_shows", methods=["GET"])
def get_all_shows():
    movie_shows = Movie_Show.objects()
    updated_movie_shows = []

    for movie_show in movie_shows:
        # Fetch the corresponding Movie object using the movie_id attribute of movie_show
        movie = Movie.objects.with_id(movie_show.movie_id.id)

        if movie:
            # Calculate the end time using the helper function
            end_time = calculate_end_time(movie_show.start_time, movie.duration)

            # Create a new dictionary and copy the fields from movie_show and movie
            updated_movie_show = {
                **movie_show.to_mongo(),
                "image_url": movie.image_url,
                "duration": movie.duration,
                "movie_name": movie.movie_name,
                "end_time": end_time,
                "movie_id": str(movie.id),  # Convert the ObjectId to a string
            }
            updated_movie_shows.append(updated_movie_show)

    # Convert the ObjectId to a string for each item in the list
    for show in updated_movie_shows:
        show["_id"] = str(show["_id"])

    # Return the Response object with a valid JSON response
    return Response(response=json.dumps(updated_movie_shows), status=200, mimetype="application/json")



# get all the shows related to a particular movie
# http://127.0.0.1:5000/movie_shows/<ObjectId:_id>
@app.route("/movie_shows/<ObjectId:_id>", methods=["GET"])
def get_related_movie_shows(_id):
    # Fetch the Movie_Show objects related to the specified Movie _id
    movie_shows = Movie_Show.objects(movie_id=_id)
    print(movie_shows)
    # Fetch the corresponding Movie object
    movie = Movie.objects.with_id(_id)  # Use with_id() to fetch the movie with the given ObjectId

    if not movie:
        return jsonify({"message": "Movie not found"}), 404

    # Create a list to store updated Movie_Show objects with additional fields
    updated_movie_shows = []

    # Update each Movie_Show object with image_url and duration from the Movie object
    for movie_show in movie_shows:
        # Calculate the end time using the helper function
        end_time = calculate_end_time(movie_show.start_time, movie.duration)

        # Create a new dictionary and copy the fields from movie_show and movie
        updated_movie_show = {
            **movie_show.to_mongo(),
            "image_url": movie.image_url,
            "duration": movie.duration,
            "movie_name": movie.movie_name,
            "end_time": end_time,
            "movie_id": str(movie.id),  # Convert the ObjectId to a string
        }
        updated_movie_shows.append(updated_movie_show)

    # Convert the ObjectId to a string for each item in the list
    for show in updated_movie_shows:
        show["_id"] = str(show["_id"])

    return jsonify(updated_movie_shows)




# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)


