from flask import Flask, request, render_template
from datetime import datetime
from dotenv import load_dotenv
import os
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables
load_dotenv()

# Create Flask app first
app = Flask(__name__)

# MongoDB connection
uri = os.getenv("MONGO_URL")
client = MongoClient(uri, server_api=ServerApi('1'))

# Test MongoDB connection
try:
    client.admin.command('ping')
    print("✅ Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("❌ Connection failed:", e)

# Route to check MongoDB connection
@app.route('/check_db')
def check_db():
    try:
        client.admin.command('ping')
        return "✅ MongoDB connection is active!"
    except Exception as e:
        return f"❌ Connection failed: {e}"

@app.route('/')
def home():
    return render_template('login.html')

# @app.route('/submit', methods=['POST'])
# def submit():
#     form_data = dict(request.form)
#     print(form_data)
#     return form_data

@app.route('/submit', methods=['POST'])
def submit():
    form_data = dict(request.form)
    print(form_data)  # Just to see what’s being received

    try:
        # Choose your database and collection name
        db = client["flask_test_db"]         # create or use existing DB
        collection = db["form_submissions"]  # create or use existing collection

        # Insert form data into MongoDB
        result = collection.insert_one(form_data)

        return f"✅ Data inserted with ID: {result.inserted_id}"
    except Exception as e:
        return f"❌ Failed to insert data: {e}"



@app.route('/view')
def view():
    try:
        db = client["flask_test_db"]
        collection = db["form_submissions"]

        # Retrieve all documents
        data = list(collection.find({}, {"_id": 0}))  # exclude _id for readability

        # Print to terminal for debugging
        print(data)

        # Return data as a simple HTML or JSON
        return {"data": data}  # Flask will return JSON automatically
    except Exception as e:
        return f"❌ Error retrieving data: {e}"





if __name__ == '__main__':
    app.run(debug=True)
