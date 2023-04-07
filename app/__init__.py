from flask import Flask,session
from app import database

app=Flask(__name__)
app.secret_key = "OurNotificationApplication"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = ''

DynamoDB=database.dynamoManager()

from app import routes