from curses.ascii import US
from os import access
import random
import string
import email
from flask import Blueprint, jsonify, request
from itsdangerous import json
import validators
from werkzeug.security import check_password_hash, generate_password_hash
from src.constants.http_satus_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from src.database import User, db
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
#from flasgger import swag_from

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth.post('/register')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    referal_code = request.json['referal_code']

    if len(password) < 6:
        return jsonify({'error':"Password id too short"}), HTTP_400_BAD_REQUEST
    
    if len(username) < 3:
        return jsonify({'error':"User id too short"}), HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({'error':"Username harus alphanumeric dan tidak pakai spasi"}), HTTP_400_BAD_REQUEST
    
    if not validators.email(email):
        return jsonify({'error':"email is not valid"}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': "Email Harus diisi"}), HTTP_409_CONFLICT
    
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': "Username harus diisi"}), HTTP_409_CONFLICT

    
    pwd_hash = generate_password_hash(password)
    ref_code = ''.join(random.choices(string.digits+string.ascii_letters, k=10))

    user = User(username=username, password=pwd_hash, email=email, referal_code=ref_code)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "User created",
        'user':{
            'username':username, 
            'email':email,
            'referal_code':user.referal_code     
        }
    }), HTTP_201_CREATED

@auth.post('/login')

def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')
    
    user = User.query.filter_by(email=email).first()

    if user:
        is_pass_correct= check_password_hash(user.password, password)

        if is_pass_correct:
            refresh=create_refresh_token(identity=user.id)
            access =create_access_token(identity=user.id)

            return jsonify({
                'user': {
                    'refresh': refresh,
                    'access': access,
                    'username': user.username,
                    'email': user.email,
                }
            }), HTTP_200_OK
    return jsonify({'error':'Wrong Credentials'}), HTTP_401_UNAUTHORIZED

@auth.get('/referalcode')
@jwt_required()
def referalcode():
    user_id = get_jwt_identity()
    access = create_access_token(identity=user_id)
    referal_code = request.json.get('referal_code', '')
    user = User.query.filter_by(referal_code=referal_code).first()

    if user:
        return jsonify({
            'username':user.username,
            'token':access
        })
    else:
        return jsonify({
            'pesan':"referal code tidak cocok"
        }), HTTP_200_OK

@auth.get('/me')
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "username": user.username,
        "email": user.email
    }), HTTP_200_OK

@auth.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_user_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        'access':access
    }), HTTP_200_OK

@auth.put('/<int:id>')
@auth.patch('/<int:id>')
@jwt_required()
def edituser(id):
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    access = create_access_token(identity=user_id)

    if not user:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    username = request.get_json().get('username', '')
    user.username = username

    db.session.commit()
    return jsonify({
        'id':user.id,
        'username':user.username,
        'access':access
    }), HTTP_200_OK

@auth.get('/username')
@jwt_required()
def findusername():
    username=request.get_json().get('username', '')
    user = User.query.filter_by(username=username).first()

    if user:
        return jsonify({
           'msg':'username ada di database',
            'user':{
            'username':user.username, 
            'email':user.email,
                 
            }
        })
    else:
        return jsonify({
            'pesan':'username tidak ditemukan'
        })


