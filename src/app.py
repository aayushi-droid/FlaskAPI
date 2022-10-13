from flask import request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from src.models import User, db
from src.schema import UserSchema
from src.config import app

limiter = Limiter(app,
                  key_func=get_remote_address)

def custom_rate_limit():
    ''' custom function for rate limit '''
    return app.config.get('CUSTOM_LIMIT', "10/minute")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# get one user
@app.route('/user/<id>', methods=['GET'])
@limiter.exempt
def get_user(id):
    """ get user by id """
    user = User.query.get(id)
    return user_schema.jsonify(user)

# get all users with custom rate limit
@app.route('/user/', methods=['GET'])
@limiter.exempt
def get_users():
    """ get all users """
    user = User.query.all()
    result = users_schema.dump(user)
    return jsonify(result)

  # get one user
@app.route('/user/<id>', methods=['GET'])
@limiter.exempt
def get_user(id):
    """ get user by id """
    user = User.query.get(id)
    return user_schema.jsonify(user)

# get all users with custom rate limit
@app.route('/user/', methods=['GET'])
@limiter.exempt
def get_users():
    """ get all users """
    user = User.query.all()
    result = users_schema.dump(user)
    return jsonify(result)
@app.route('/user', methods=['POST'])
@limiter.limit(custom_rate_limit)
def create_user():
    ''' create new user '''
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    new_user = User(username, password, email)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

# update the user
@app.route('/user/<int:id>', methods=['PUT'])
@limiter.limit(custom_rate_limit)
def update_user(id):
    """ update user by id """
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
@limiter.limit(custom_rate_limit)
def delete_user(id):
    ''' delete the user '''
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)
