from flask import jsonify, abort, request
from models.part import PartModel
from flask_restful import reqparse

part_parser = reqparse.RequestParser()  
part_parser.add_argument('number', type=int, required=True, help="number cannot be blank!")
part_parser.add_argument('description', type=str, required=True, help="description cannot be blank!")
part_parser.add_argument('route_id', type=int, required=True, help="route_id cannot be blank!")
part_parser.add_argument('category_id', type=int, required=True, help="category_id cannot be blank!")


def get_part_by_id(part_id):
    part = PartModel.get_by_id(part_id)

    if not part:
        abort(404, message="Part not found")

    response = {
        "number": part.number,  
        "description": part.description,  
        "_id": part.id,
        "category_id": part.category_id, 
        "route_id":    part.route_id,
        "category": {
            "name": part.categories.name,
            "type": part.categories._type.value,
            "_id":  part.categories.id
        },
        "route": {
            "name": part.routes.name,
            "description": part.routes.description,  
            "_id": part.routes.id
        }
    }
    return jsonify(response)


def get_all_parts():
    parts = PartModel.query.all()

    response = {
        "items": [
            {
                "number": part.number,  
                "description": part.description,  
                "_id": part.id,
                "category_id":part.category_id,
                "route_id":part.route_id 
            } for part in parts
        ]
    }
    return jsonify(response)


def get_paginated_parts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    paginated_parts = PartModel.query.paginate(page=page, per_page=per_page, error_out=False)

    response = {
        "items": [
            {
                "number": part.number,  
                "description": part.description,  
                "_id": part.id,
                "category_id":part.category_id,
                "route_id":part.route_id,
                "category": {
                    "name": part.categories.name,
                    "_id": part.categories.id,
                    "type": part.categories._type.value  
                },
                "route": {
                    "name": part.routes.name,
                    "description": part.routes.description,
                    "_id": part.routes.id
                }
            } for part in paginated_parts.items
        ],
        "pagination": {
            "page": paginated_parts.page,
            "size": paginated_parts.per_page,
            "total": paginated_parts.total,
            "has_more": paginated_parts.has_next
        }
    }
    return jsonify(response)

def create_part():
    data = part_parser.parse_args()
    
    new_part = PartModel(
        number=data['number'],          
        description=data['description'],  
        category_id=data['category_id'],  
        route_id=data['route_id'],        
    )
    new_part.save()

    response = {
        "number": new_part.number,
        "description": new_part.description,
        "_id": new_part.id,
        "category_id": new_part.category_id,
        "route_id": new_part.route_id
    }

    return jsonify(response)


def update_part(part_id):
    data = part_parser.parse_args()
    
    part = PartModel.get_by_id(part_id)
    
    if not part:
        abort(404, description="Part not found")
    
    part.update(**data)  

    response = {
        "number": part.number,
        "description": part.description,
        "_id": part.id,
        "category_id": part.category_id,
        "route_id": part.route_id
    }
    
    return jsonify(response)
   
def delete_part(part_id):  
    part = PartModel.get_by_id(part_id) 
    if not part:
        abort(404, message="Part not found")
    part.delete()
    return jsonify({'message': 'Part deleted'})

def delete_all_parts():  
    part_records = PartModel.query.all() 
    for part in part_records:
        part.delete()
    return jsonify({'message': 'All parts deleted'})
