from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '4f1d7cfcc8ee00efeb6c36b9'

from application import routes