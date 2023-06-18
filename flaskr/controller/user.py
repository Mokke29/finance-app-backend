from urllib import response
from flaskr.utils.db_conn import db
from flask import Blueprint, request, jsonify, make_response
from flaskr.model.user import User
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from flaskr.utils.safe_str_cmp import safe_str_cmp
import os

route = Blueprint("user_route", __name__, static_folder="static")


@route.post('/create')
def create_user():
    data = request.get_json()
    new_user = User.create(data['username'], data['password'])
    if new_user:
        user = User.get_by_username(new_user)
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)
        response = make_response(
            {"err": False, 'msg': f'New user created #{new_user}'})
        response.set_cookie('access_token_cookie',
                            access_token, secure=True, samesite='None')
        response.set_cookie('refresh_token_cookie',
                            refresh_token, secure=True, samesite='None')
        response.headers.add('Access-Control-Allow-Headers',
                             'x-www-form-urlencoded, Origin, X-Requested-With, Content-Type, Accept, Authorization')
        return response
    else:
        return jsonify(err=True, msg='User already exists...')


@route.delete('/delete')
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    user = User.get_by_id(user_id)
    if user.delete():
        return jsonify('User deleted successfully!')
    else:
        return jsonify('Something went wrong, please try again later...')


@route.post('/login')
def login():
    data = request.get_json()
    found_user = User.get_by_username(data.get("username"))
    if found_user and safe_str_cmp(found_user.password, data.get("password")):
        access_token = create_access_token(
            identity=found_user.id, fresh=True)
        refresh_token = create_refresh_token(found_user.id)
        response = make_response(
            {'msg': 'Logged in!', "username": found_user.username})
        response.set_cookie('access_token_cookie',
                            access_token, secure=True, samesite='None')
        response.set_cookie('refresh_token_cookie',
                            refresh_token, secure=True, samesite='None')
        response.headers.add('Access-Control-Allow-Headers',
                             'x-www-form-urlencoded, Origin, X-Requested-With, Content-Type, Accept, Authorization')
        return response
    else:
        return jsonify({'error': 'Wrong username or password', "status": "unauthorized"}), 200


@route.get('/logout')
def logout():

    response = make_response({'msg': 'Logged out!'})
    response.delete_cookie('access_token_cookie',
                           secure=True, samesite='None')
    response.delete_cookie('refresh_token_cookie',
                           secure=True, samesite='None')

    return response


@route.delete('/get-user')
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = User.get_by_id(user_id)
    print(user.username)
    return "200"
