from flask import jsonify, abort, request
from models.user import UserModel  
from models.role import RoleModel  
from models.location import LocationModel  

from flask_restful import reqparse

# Define request parser for User
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True, help="username cannot be blank!")
user_parser.add_argument('first_name', type=str, required=True, help="first_name cannot be blank!")
user_parser.add_argument('last_name', type=str, required=True, help="last_name cannot be blank!")
user_parser.add_argument('email', type=str, required=True, help="email cannot be blank!")
user_parser.add_argument('password', type=str, required=True, help="password cannot be blank!")
user_parser.add_argument('role_id', type=int, required=True, help="role_id cannot be blank!")
user_parser.add_argument('disabled', type=bool, default=False, help="disabled cannot be blank!")
user_parser.add_argument('work_location_ids', type=list, location='json', help="work_location_ids must be a list!")

def get_user_by_id(user_id):
    user = UserModel.get_by_id(user_id)

    if not user:
        abort(404, message="User not found")

    response = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "emailaddress": user.email,
        "_id": user.id,
        "role_id": user.role_id,
        "disabled": user.disabled,
        "work_location_ids": user.work_location_ids
    }
    return jsonify(response)


def get_all_users():
    users = UserModel.query.all()

    response = {
        "items": [
            {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "emailaddress": user.email,
                "_id": user.id,
                "role_id": user.role_id,
                "disabled": user.disabled,
                "work_location_ids": user.work_location_ids
            } for user in users
        ]
    }
    return jsonify(response)

def get_paginated_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    paginated_users = UserModel.query.paginate(page=page, per_page=per_page, error_out=False)

    response = {
        "items": [
            {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "emailaddress": user.email,
                "_id": user.id,
                "role_id": user.role_id,
                "disabled": user.disabled,
                "work_location_ids": user.work_location_ids
            } for user in paginated_users.items
        ],
        "pagination": {
            "page": paginated_users.page,
            "size": paginated_users.per_page,
            "total": paginated_users.total,
            "has_more": paginated_users.has_next
        }
    }
    return jsonify(response)

def get_current_user(user_id):
    user = UserModel.get_by_id(user_id)

    if not user:
        abort(404, message="User not found")

    role = RoleModel.get_by_id(user.role_id)  # Fetch role details
    work_locations = LocationModel.query.filter(LocationModel.id.in_(user.work_location_ids)).all()  # Fetch work locations

    response = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "_id": user.id,
        "role_id": user.role_id,
        "disabled": user.disabled,
        "work_location_ids": user.work_location_ids,
        "role": {
            "name": role.name,
            "description": role.description,
            "_id": role.id,
        },
        "work_locations": [
            {
                "_id": wl.id,
                "name": wl.name
            } for wl in work_locations
        ]
    }
    return jsonify(response)


def create_user():
    data = user_parser.parse_args()
    
    new_user = UserModel(
        username=data['username'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data['password'], 
        role_id=data['role_id'],
        disabled=data['disabled'],
        work_location_ids=data['work_location_ids']
    )
    new_user.save()

    response = {
        "username": new_user.username,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "emailaddress": new_user.email,
        "_id": new_user.id,
        "role_id": new_user.role_id,
        "disabled": new_user.disabled,
        "work_location_ids": new_user.work_location_ids
    }

    return jsonify(response)

def update_user(user_id):
    data = user_parser.parse_args()
    user = UserModel.get_by_id(user_id)
    
    if not user:
        abort(404, message="User not found")
        
    user.username = data['username']
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.emailaddress = data['email']
    if data['password']:
        user.password = data['password']  
    user.role_id = data['role_id']
    user.disabled = data['disabled']
    user.work_location_ids = data['work_location_ids']
    
    user.update(**data)
    
    response = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "emailaddress": user.email,
        "_id": user.id,
        "role_id": user.role_id,
        "disabled": user.disabled,
        "work_location_ids": user.work_location_ids
    }
    
    return jsonify(response)

def update__current_user(user_id):
    data = user_parser.parse_args()  #
    user = UserModel.get_by_id(user_id)  
    
    if not user:
        abort(404, message="User not found")  
    

    user.username = data['username']
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.emailaddress = data['emailaddress'] 
    if data['password']:
        user.password = data['password']  
    user.role_id = data['role_id']
    user.disabled = data['disabled']
    user.work_location_ids = data['work_location_ids']
    
    user.update(**data)  
    
    response = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "disabled": user.disabled,
        "_id": user.id,
        "email": user.email,  
        "role_id": user.role_id, 
        "work_location_ids": user.work_location_ids if user.work_location_ids else []  
    }
    
    return jsonify(response)


def delete_user(user_id):  
    user = UserModel.get_by_id(user_id) 
    if not user:
        abort(404, message="User not found")
    user.delete()
    return jsonify({'message': 'User deleted'})

def delete_all_users():  
    user_records = UserModel.query.all() 
    for user in user_records:
        user.delete()
    return jsonify({'message': 'All users deleted'})
