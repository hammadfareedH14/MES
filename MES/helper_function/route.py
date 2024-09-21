
from flask import jsonify,abort,request
from models.route import RouteModel
from flask_restful import reqparse

route_parser = reqparse.RequestParser()
route_parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
route_parser.add_argument('description', type=str, required=True, help="Description cannot be blank!")

def get_route_by_id(route_id):
    route = RouteModel.get_by_id(route_id)
    if not route:
        abort(404, message="Route not found")
    return jsonify({
        "name": route.name,
        "description": route.description,
        "_id": str(route.id)
    })

def get_all_routes():
    routes = RouteModel.query.all()
    response = {
        "items": [
            {
                "name": route.name,
                "description": route.description,
                "_id": str(route.id)
            } for route in routes
        ]
    }
    return jsonify(response)

def get_paginated_routes():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    paginated_routes = RouteModel.query.paginate(page=page, per_page=per_page, error_out=False)
    response = {
        "items": [
            {
                "name": route.name,
                "description": route.description,
                "_id": str(route.id)
            } for route in paginated_routes.items
        ],
        "pagination": {
            "page": paginated_routes.page,
            "size": paginated_routes.per_page,
            "total": paginated_routes.total,
            "has_more": paginated_routes.has_next
        }
    }
    return jsonify(response)

def create_route():
    data= route_parser.parse_args()
    new_route = RouteModel(name=data['name'], description=data["description"])
    new_route.save()
    return jsonify({'message': 'Route created', 'id': new_route.id})

def update_route(route_id):
    data= route_parser.parse_args()
    route = RouteModel.get_by_id(route_id)
    if not route:
        abort(404, message="Route not found")
    route.update(**data)
    return jsonify({'message': 'Route updated', 'id': route.id})

def delete_route(route_id):
    route = RouteModel.get_by_id(route_id)
    if not route:
        abort(404, message="Route not found")
    route.delete()
    return jsonify({'message': 'Route deleted'})
