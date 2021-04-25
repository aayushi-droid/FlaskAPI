from flask_marshmallow import Marshmallow

from src.config import app

ma = Marshmallow(app)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'email')


