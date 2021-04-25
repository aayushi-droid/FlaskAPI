import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))

def create_app():
    app = Flask(__name__)

    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    return app

app = create_app()