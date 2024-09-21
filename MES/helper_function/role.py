from flask import jsonify, abort, request
from models.role import RoleModel
from flask_restful import reqparse

role_parser = reqparse.RequestParser()  
role_parser.add_argument('name', type=str, required=True, help="name cannot be blank!")
role_parser.add_argument('description', type=str, required=True, help="description cannot be blank!")

def get_role_by_id(role_id):
    role = RoleModel.get_by_id(role_id)

    if not role:
        abort(404, message="Role not found")

    response = {
        "name": role.name,  
        "description": role.description,
        "_id": role.id,
    }
    return jsonify(response)


def get_all_roles():
    roles = RoleModel.query.all()

    response = {
        "items": [
            {
                "name": role.name,
                "description": role.description,
                "_id": str(role.id)
            } for role in roles
        ]
    }
    return jsonify(response)


def get_paginated_roles():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    paginated_roles = RoleModel.query.paginate(page=page, per_page=per_page, error_out=False)

    response = {
        "items": [
            {
                "name": role.name,
                "description": role.description,
                "_id": str(role.id),
            } for role in paginated_roles.items
        ],
        "pagination": {
            "page": paginated_roles.page,
            "size": paginated_roles.per_page,
            "total": paginated_roles.total,
            "has_more": paginated_roles.has_next
        }
    }
    return jsonify(response)


def create_role():
    data = role_parser.parse_args()
    
    new_role = RoleModel(
        name=data['name'],
        description=data['description'],  
    )
    new_role.save()

    response = {
        "name": new_role.name,
        "description": new_role.description,
    }

    return jsonify(response)


def update_role(role_id):
    data = role_parser.parse_args()
    role = RoleModel.get_by_id(role_id)
    
    if not role:
        abort(404, message="Role not found")
        
    role.update(**data)  
    
    response = {
        "name": role.name,
        "description": role.description,
    }
    
    return jsonify(response)

def delete_role(role_id):  
    role = RoleModel.get_by_id(role_id) 
    if not role:
        abort(404, message="Role not found")
    role.delete()
    return jsonify({'message': 'Role deleted'})

def delete_all_roles():  
    role_records = RoleModel.query.all() 
    for role in role_records:
        role.delete()
    return jsonify({'message': 'All roles deleted'})
