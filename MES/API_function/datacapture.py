from flask import jsonify, request
from flask_restful import reqparse, abort
from datetime import datetime
from models.datacapture import DataCaptureModel  # Assuming the model is renamed to DataCaptureModel

# Define the request parser for DataCapture
datacapture_parser = reqparse.RequestParser()
datacapture_parser.add_argument('action', type=str, required=True, help="action cannot be blank")  # New field
datacapture_parser.add_argument('value', type=str, required=True, help="value cannot be blank")  # New field
datacapture_parser.add_argument('worklocation_id', type=int, required=True, help="worklocation_id cannot be blank")  # New field

def get_datacapture_by_id(datacapture_id):
    # Fetch the DataCapture record by its ID
    datacapture = DataCaptureModel.get_by_id(datacapture_id)

    if not datacapture:
        abort(404, message="Data capture not found")

    # Construct the nested response with related entities
    response = {
        "action": datacapture.action,
        "value": datacapture.value,
        "_id": datacapture.id,
        "work_operation_id": str(datacapture.work_operation_id),
        "work_operation": {
            "start_timestamp": datacapture.start_timestamp,
            "complete_timestamp": datacapture.complete_timestamp,
            "status": datacapture.status,
            "mark_status": datacapture.mark_status,
            "comment": {
                "type": datacapture.comment_type,
                "comment": datacapture.comment,
                "timestamp": datacapture.comment_timestamp
            },
            "_id": datacapture.id,
            "work_instruction_id": datacapture.work_instruction_id,
            "user_id": datacapture.user_id,
            "work_instruction": {
                "description": datacapture.work_instruction.description,
                "_id": datacapture.work_instruction.id,
                "category_id": datacapture.work_instruction.category_id,
                "work_location_id": datacapture.work_instruction.work_location_id,
                "parts": [
                    {
                        "part_id": part.id,
                        "image_url": part.image_url,
                        "part": {
                            "number": part.number,
                            "description": part.description,
                            "_id": part.id,
                            "category_id": part.category_id,
                            "route_id": part.route_id,
                            "category": {
                                "name": part.category.name,
                                "type": part.category.type,
                                "_id": part.category.id
                            },
                            "route": {
                                "name": part.route.name,
                                "description": part.route.description,
                                "_id": part.route.id
                            }
                        }
                    } for part in datacapture.work_instruction.parts
                ],
                "category": {
                    "name": datacapture.work_instruction.category.name,
                    "type": datacapture.work_instruction.category.type,
                    "_id": datacapture.work_instruction.category.id
                },
                "work_location": {
                    "name": datacapture.work_instruction.work_location.name,
                    "_id": datacapture.work_instruction.work_location.id,
                    "station_id": datacapture.work_instruction.work_location.station_id,
                    "station": {
                        "name": datacapture.work_instruction.work_location.station.name,
                        "_id": datacapture.work_instruction.work_location.station.id,
                        "line_id": datacapture.work_instruction.work_location.station.line_id,
                        "line": {
                            "name": datacapture.work_instruction.work_location.station.line.name,
                            "_id": datacapture.work_instruction.work_location.station.line.id,
                            "shop_id": datacapture.work_instruction.work_location.station.line.shop_id,
                            "shop": {
                                "name": datacapture.work_instruction.work_location.station.line.shop.name,
                                "_id": datacapture.work_instruction.work_location.station.line.shop.id
                            }
                        }
                    }
                }
            },
            "user": {
                "username": datacapture.user.username,
                "first_name": datacapture.user.first_name,
                "last_name": datacapture.user.last_name,
                "disabled": datacapture.user.disabled,
                "_id": datacapture.user.id,
                "email": datacapture.user.email,
                "role_id": datacapture.user.role_id,
                "work_location_ids": [location.id for location in datacapture.user.work_locations],
                "role": {
                    "name": datacapture.user.role.name,
                    "description": datacapture.user.role.description,
                    "_id": datacapture.user.role.id,
                    "access": datacapture.user.role.access
                },
                "work_locations": [
                    {
                        "name": location.name,
                        "_id": location.id
                    } for location in datacapture.user.work_locations
                ]
            }
        }
    }

    return jsonify(response)

# Function to retrieve all DataCaptures
def get_all_datacaptures():
    datacaptures = DataCaptureModel.query.all()

    response = {
        "items": [
            {
                "action": datacapture.action,
                "value": datacapture.value,
                "_id": datacapture.id,
                "work_operation_id": datacapture.work_instruction_id
            } for datacapture in datacaptures
        ]
    }
    return jsonify(response)


# Function to retrieve paginated DataCaptures
def get_paginated_datacaptures():
    page = int(request.args.get('page', 0))
    size = int(request.args.get('size', 10))

    paginated_datacaptures = DataCaptureModel.query.paginate(page=page, per_page=size, error_out=False)

    response = {
        "items": [
            {
                "action": datacapture.action,
                "value": datacapture.value,
                "_id": datacapture.id,
                "work_operation_id": datacapture.work_instruction_id,
                "work_operation": {
                    "start_timestamp": datacapture.start_timestamp.isoformat(),
                    "complete_timestamp": datacapture.complete_timestamp.isoformat(),
                    "status": datacapture.status,
                    "mark_status": datacapture.mark_status,
                    "comment": {
                        "type": datacapture.comment_type,
                        "comment": datacapture.comment_text,
                        "timestamp": datacapture.comment_timestamp.isoformat()
                    },
                    "_id": datacapture.work_operation_id,
                    "work_instruction_id": datacapture.work_instruction_id,
                    "user_id": datacapture.user_id,
                    "work_instruction": {
                        "description": datacapture.work_instruction.description,
                        "_id": datacapture.work_instruction.id,
                        "category_id": datacapture.work_instruction.category_id,
                        "work_location_id": datacapture.work_instruction.work_location_id,
                        "parts": [
                            {
                                "part_id": part.id,
                                "image_url": part.image_url,
                                "part": {
                                    "number": part.number,
                                    "description": part.description,
                                    "_id": part.id,
                                    "category_id": part.category_id,
                                    "route_id": part.route_id,
                                    "category": {
                                        "name": part.category.name,
                                        "type": part.category.type,
                                        "_id": part.category.id
                                    },
                                    "route": {
                                        "name": part.route.name,
                                        "description": part.route.description,
                                        "_id": part.route.id
                                    }
                                }
                            } for part in datacapture.work_instruction.parts
                        ],
                        "category": {
                            "name": datacapture.work_instruction.category.name,
                            "type": datacapture.work_instruction.category.type,
                            "_id": datacapture.work_instruction.category.id
                        },
                        "work_location": {
                            "name": datacapture.work_instruction.work_location.name,
                            "_id": datacapture.work_instruction.work_location.id,
                            "station_id": datacapture.work_instruction.work_location.station_id,
                            "station": {
                                "name": datacapture.work_instruction.work_location.station.name,
                                "_id": datacapture.work_instruction.work_location.station.id,
                                "line_id": datacapture.work_instruction.work_location.station.line_id,
                                "line": {
                                    "name": datacapture.work_instruction.work_location.station.line.name,
                                    "_id": datacapture.work_instruction.work_location.station.line.id,
                                    "shop_id": datacapture.work_instruction.work_location.station.line.shop_id,
                                    "shop": {
                                        "name": datacapture.work_instruction.work_location.station.line.shop.name,
                                        "_id": datacapture.work_instruction.work_location.station.line.shop.id
                                    }
                                }
                            }
                        }
                    },
                    "user": {
                        "username": datacapture.user.username,
                        "first_name": datacapture.user.first_name,
                        "last_name": datacapture.user.last_name,
                        "disabled": datacapture.user.disabled,
                        "_id": datacapture.user.id,
                        "email": datacapture.user.email,
                        "role_id": datacapture.user.role_id,
                        "work_location_ids": [loc.id for loc in datacapture.user.work_locations],
                        "role": {
                            "name": datacapture.user.role.name,
                            "description": datacapture.user.role.description,
                            "_id": datacapture.user.role.id,
                            "access": [access.name for access in datacapture.user.role.access]
                        },
                        "work_locations": [
                            {
                                "name": location.name,
                                "_id": location.id
                            } for location in datacapture.user.work_locations
                        ]
                    }
                }
            } for datacapture in paginated_datacaptures.items
        ],
        "pagination": {
            "page": page,
            "size": size,
            "total": paginated_datacaptures.total,
            "has_more": paginated_datacaptures.has_next
        }
    }

    return jsonify(response)


def create_datacapture():
    data = datacapture_parser.parse_args()
    
    new_datacapture = DataCaptureModel(
    action=data["action"], 
    value=data["value"], 
    work_operation_id = data["work_instruction_id"]  
    )

    new_datacapture.save()

    response = {
        "action": data["action"], 
        "value": data["value"], 
        "_id": new_datacapture.id,  
        "work_operation_id": data["work_instruction_id"]
    }

    return jsonify(response)


def update_datacapture(datacapture_id):
    data = datacapture_parser.parse_args()
    
    # Find the existing data capture by ID
    newdatacapture = DataCaptureModel.get_by_id(datacapture_id)
    
    if not datacapture_id:
        return jsonify({"message": "Data capture not found"}), 404

    # Update the fields
    
    newdatacapture.update(**data)    

    response = {
        "action": newdatacapture.action,
        "value": newdatacapture.value,
        "_id": newdatacapture.id,
        "work_operation_id": newdatacapture.work_instruction_id
    }

    return jsonify(response)

def delete_datacapture(datacapture_id):
    datacapture = DataCaptureModel.get_by_id(datacapture_id)

    if not datacapture:
        abort(404, message="Data capture not found")

    datacapture.delete()
    return jsonify({'message': 'Data capture deleted'})

# Function to delete all DataCaptures
def delete_all_datacaptures():
    datacapture_records = DataCaptureModel.query.all()
    for datacapture in datacapture_records:
        datacapture.delete()

    return jsonify({'message': 'All data captures deleted'})
