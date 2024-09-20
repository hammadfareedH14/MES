from flask import jsonify, abort,request
from models.location import LocationModel
from flask_restful import reqparse

location_parser = reqparse.RequestParser()
location_parser.add_argument('name', type=str, required=True, help="name cannot be blank!")
location_parser.add_argument('station_id', type=int, required=True, help="station_id cannot be blank!")

def get_location_by_id(location_id):
    location = LocationModel.get_by_id(location_id)
    if not location:
        abort(404, description="Location not found")
    
    # Prepare response with station, line, and shop details
    response = {
        "name": location.name,
        "_id": location.id,
        "station_id": location.stations.id,
        "station": {
            "name": location.stations.name,
            "_id": location.stations.id,
            "line_id": location.stations.lines.id,
            "line": { 
                "name": location.stations.lines.name,
                "_id": location.stations.lines.id,
                "shop_id": location.stations.lines.shops.id,
                "shop": {
                    "name": location.stations.lines.shops.name,
                    "_id": location.stations.lines.shops.id
                }
            }
        }
    }
    return jsonify(response)

def get_all_locations():
    locations = LocationModel.query.all()

    response = {
        "items": [
            {
                "name": location.name,
                "_id": location.id,
                "station_id": location.stations.id,
                "station": {
                    "name": location.stations.name,
                    "_id": location.stations.id,
                    "line_id": location.stations.lines.id,
                    "line": {
                        "name": location.stations.lines.name,
                        "_id": location.stations.lines.id,
                        "shop_id": location.stations.lines.shops.id,
                        "shop": {
                            "name": location.stations.lines.shops.name,
                            "_id": location.stations.lines.shops.id
                        }
                    }
                }
            } for location in locations
        ]
    }
    return jsonify(response)

def get_paginated_locations():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    paginated_locations = LocationModel.query.paginate(page=page, per_page=per_page, error_out=False)

    response = {
        "items": [
            {
                "name": location.name,
                "_id": location.id,
                "station_id": location.stations.id,
                "station": {
                    "name": location.stations.name,
                    "_id": location.stations.id,
                    "line_id": location.stations.lines.id,
                    "line": {
                        "name": location.stations.lines.name,
                        "_id": location.stations.lines.id,
                        "shop_id": location.stations.lines.shops.id,
                        "shop": {
                            "name": location.stations.lines.shops.name,
                            "_id": location.stations.lines.shops.id
                        }
                    }
                }
            } for location in paginated_locations.items
        ],
        "pagination": {
            "page": paginated_locations.page,
            "size": paginated_locations.per_page,
            "total": paginated_locations.total,
            "has_more": paginated_locations.has_next
        }
    }
    return jsonify(response)

def create_location():
    data = location_parser.parse_args()
    new_location = LocationModel(name=data['name'], station_id=data['station_id'])
    new_location.save()
    return jsonify({'message': 'Location created', 'id': new_location.id})

def update_location(location_id):
    data = location_parser.parse_args()
    location = LocationModel.get_by_id(location_id)
    if not location:
        abort(404, message="Location not found")
    location.update(**data)
    return jsonify({'message': 'Location updated', 'id': location.id})

def delete_location(location_id):
    location = LocationModel.get_by_id(location_id)
    if not location:
        abort(404, message="Location not found")
    location.delete()
    return jsonify({'message': 'Location deleted'})

def delete_all_location():
        location_records = LocationModel.query.all()  
        for location in location_records:
            location.delete()
        return jsonify({'message': 'All locations deleted'})

