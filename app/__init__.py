"""
SpotifyPythonControl
By: Amahlaka

Disclaimer:
I hold no responsibility if this grinds up your cat, burns your house or pops your eye etc etc...
10.11.2018
"""
import requests
import config
from flask import Flask


app = Flask(__name__)
app.secret_key = ''  # Paste the generated code here

from app import authenticater