from flask import Flask

app = Flask(__name__)
app.secret_key = "120893u1023821-3183-2103"
from app import routes