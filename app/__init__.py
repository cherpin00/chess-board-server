from flask import Flask

app = Flask(__name__)

from app import views

app.run(debug=True, host="0.0.0.0")