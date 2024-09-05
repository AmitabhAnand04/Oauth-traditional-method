from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from jwt import PyJWT
import datetime
from functools import wraps
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt_raiser = PyJWT()


# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    token = db.Column(db.String(500), nullable=True)  # To store the JWT token for each user

# User registration API
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Hash the password
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create and store user
    user = User(username=username, password=hashed_pw)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

# User login API (generates and returns a JWT token)
@app.route('/createtoken', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):

        # payload 
        payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }

        key = app.config['SECRET_KEY']
        algorithm="HS256"

        # Generate JWT token
        token = jwt_raiser.encode(
            payload=payload,
            key=key,
            algorithm=algorithm
        )
        user.token = token  # Store the token in the database
        db.session.commit()
        
        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "Invalid credentials!"}), 401

# Token verification decorator
def token_required(f):
    @wraps(f)  # Ensure function retains its original name
    def decorator(*args, **kwargs):
        token = request.headers.get('x-access-token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Decode the token
            data = jwt_raiser.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorator


# Get Token API (retrieve the token for a user)
@app.route('/gettoken', methods=['POST'])
def get_token():
    data = request.get_json()
    username = data.get('username')

    user = User.query.filter_by(username=username).first()

    if user:
        if user.token:
            return jsonify({"token": user.token}), 200
        else:
            return jsonify({"message": "No token found for this user!"}), 404
    else:
        return jsonify({"message": "User not found!"}), 404


# Revoke token API (invalidate the token)
@app.route('/revoketoken', methods=['POST'])
@token_required
def revoke_token(current_user):
    current_user.token = None  # Clear the token
    db.session.commit()
    return jsonify({"message": "token revoked successfully!"}), 200



# Protected dashboard API (requires a valid token)
@app.route('/dashboard', methods=['GET'])
@token_required
def dashboard(current_user):
    return jsonify({"message": f"Welcome to the protected dashboard, {current_user.username}!"})

if __name__ == '__main__':
    app.run(debug=True, port=9000)