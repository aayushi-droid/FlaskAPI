import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
basedir = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))

app.debug = True
# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


# model class
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return f"<User {self.username}>"


# schemas
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'email')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


# create a user
@app.route('/user', methods=['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    new_user = User(username, password, email)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


# get all users
@app.route('/user/', methods=['GET'])
def get_users():
    user = User.query.all()
    result = users_schema.dump(user)
    return jsonify(result)


# get one user
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


# update the user
@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)

    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    user.username = username
    user.password = password
    user.email = email

    db.session.commit()

    return user_schema.jsonify(user)


# delete the user
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)


if __name__ == '__main__':
    app.run()

    