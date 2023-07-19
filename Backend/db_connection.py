from flask import Flask
import mongoengine

app = Flask(__name__)

# Set up the default MongoDB connection
app.config['MONGODB_SETTINGS'] = {
    'db': 'tickethubDB',
    # 'host': 'your_mongodb_uri',  # e.g., 'mongodb://localhost:27017/your_database_name'
}

mongoengine.connect(db=app.config['MONGODB_SETTINGS']['db'], host=app.config['MONGODB_SETTINGS']['host'])
