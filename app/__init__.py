import requests
import config
from flask import Flask


app = Flask(__name__)
app.secret_key = ''  # Generate a secret key here

from app import authenticater