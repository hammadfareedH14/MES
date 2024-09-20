from flask import jsonify, request
from flask_restful import reqparse, abort
from datetime import datetime
from models.operation import OperationModel  

operation_parser = reqparse.RequestParser() # Define the request parser
operation_parser.add_argument('start_timestamp', type=str, required=True, help="start_timestamp cannot be blank")
operation_parser.add_argument('complete_timestamp', type=str, required=True, help="complete_timestamp cannot be blank")
operation_parser.add_argument('status', type=str, required=True, help="status cannot be blank")
operation_parser.add_argument('mark_status', type=str, required=True, help="mark_status cannot be blank")
operation_parser.add_argument('comment', type=dict, required=True, help="comment cannot be blank")  
operation_parser.add_argument('work_instruction_id', type=str, required=True, help="work_instruction_id cannot be blank")
operation_parser.add_argument('user_id', type=str, required=True, help="user_id cannot be blank")


def get_operation_by_id(operation_id):  
    operation = OperationModel.get_by_id(operation_id)  

    if not operation:
        abort(404, message="Operation not found")

    response = {
        "start_timestamp": operation.start_timestamp,  
        "complete_timestamp": operation.complete_timestamp,  
        "status": operation.status,  
        "mark_status": operation.mark_status,
        "comment": {
            "type": operation.comment_type, 
            "comment": operation.comment,
            "timestamp": operation.comment_timestamp
        },
        "_id": operation.id,
        "work_instruction_id": operation.work_instruction_id,  
        "user_id": operation.user_id,
        "work_instruction": {
            "description": operation.work_instruction.description,
            "_id": operation.work_instruction.id,
            "category_id": operation.work_instruction.category_id,
            "work_location_id": operation.work_instruction.work_location_id,
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
                            "type": part.category._type.value,
                            "_id": part.category.id
                        },
                        "route": {
                            "name": part.route.name,
                            "description": part.route.description,
                            "_id": part.route.id
                        }
                    }
                } for part in operation.work_instruction.parts
            ],
            "category": {
                "name": operation.work_instruction.category.name,
                "type": operation.work_instruction.category._type.value,
                "_id": operation.work_instruction.category.id
            },
            "work_location": {
                "name": operation.work_instruction.work_location.name,
                "_id": operation.work_instruction.work_location.id,
                "station_id": operation.work_instruction.work_location.station_id,
                "station": {
                    "name": operation.work_instruction.work_location.station.name,
                    "_id": operation.work_instruction.work_location.station.id,
                    "line_id": operation.work_instruction.work_location.station.line_id,
                    "line": {
                        "name": operation.work_instruction.work_location.station.line.name,
                        "_id": operation.work_instruction.work_location.station.line.id,
                        "shop_id": operation.work_instruction.work_location.station.line.shop_id,
                        "shop": {
                            "name": operation.work_instruction.work_location.station.line.shop.name,
                            "_id": operation.work_instruction.work_location.station.line.shop.id
                        }
                    }
                }
            }
        },
        "user": {
            "username": operation.user.username,
            "first_name": operation.user.first_name,
            "last_name": operation.user.last_name,
            "disabled": operation.user.disabled,
            "_id": operation.user.id,
            "email": operation.user.email,
            "role_id": operation.user.role_id,
            "work_location_ids": operation.user.work_location_ids,
            "role": {
                "name": operation.user.role.name,
                "description": operation.user.role.description,
                "_id": operation.user.role.id,
            },
            "work_locations": operation.user.work_locations 
        }
    }

    return jsonify(response)


from flask import jsonify

def get_all_operations():  
    operations = OperationModel.query.all()  

    response = {
        "items": [
            {
                "start_timestamp": operation.start_timestamp.isoformat(),  
                "complete_timestamp": operation.complete_timestamp.isoformat(), 
                "status": operation.status,
                "mark_status": operation.mark_status,
                "comment": {
                    "type": operation.comment_type,  
                    "comment": operation.comment_text,  
                    "timestamp": operation.comment_timestamp.isoformat() 
                },
                "_id": operation.id,
                "work_instruction_id": operation.work_instruction_id,
                "user_id": operation.user_id
            } for operation in operations
        ]
    }
    return jsonify(response)


def get_paginated_operations():  
    page = int(request.args.get('page', 0))
    size = int(request.args.get('size', 10))

    paginated_operations = OperationModel.query.paginate(page=page, per_page=size, error_out=False)  
    # operations = operations_query.items
    
    response = {
        "items": [
            {
                "start_timestamp": operation.start_timestamp,  # Include these fields in your model
                "complete_timestamp": operation.complete_timestamp,
                "status": operation.status,
                "mark_status": operation.mark_status,
                "comment": {
                    "type": operation.comment_type,  # Adjust based on how you handle comments
                    "comment": operation.comment,
                    "timestamp": operation.comment_timestamp
                },
                "_id": operation.id,
                "work_instruction_id": operation.work_instruction_id,
                "user_id": operation.user_id,
                "work_instruction": {
                    "description": operation.work_instruction.description,
                    "_id": operation.work_instruction.id,
                    "category_id": operation.work_instruction.category_id,
                    "work_location_id": operation.work_instruction.work_location_id,
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
                                    "type": part.category._type.value,
                                    "_id": part.category.id
                                },
                                "route": {
                                    "name": part.route.name,
                                    "description": part.route.description,
                                    "_id": part.route.id
                                }
                            }
                        } for part in operation.work_instruction.parts
                    ],
                    "category": {
                        "name": operation.work_instruction.category.name,
                        "type": operation.work_instruction.category._type.value,
                        "_id": operation.work_instruction.category.id
                    },
                    "work_location": {
                        "name": operation.work_instruction.work_location.name,
                        "_id": operation.work_instruction.work_location.id,
                        "station_id": operation.work_instruction.work_location.station_id,
                        "station": {
                            "name": operation.work_instruction.work_location.station.name,
                            "_id": operation.work_instruction.work_location.station.id,
                            "line_id": operation.work_instruction.work_location.station.line_id,
                            "line": {
                                "name": operation.work_instruction.work_location.station.line.name,
                                "_id": operation.work_instruction.work_location.station.line.id,
                                "shop_id": operation.work_instruction.work_location.station.line.shop_id,
                                "shop": {
                                    "name": operation.work_instruction.work_location.station.line.shop.name,
                                    "_id": operation.work_instruction.work_location.station.line.shop.id
                                }
                            }
                        }
                    }
                },
                "user": {
                    "username": operation.user.username,
                    "first_name": operation.user.first_name,
                    "last_name": operation.user.last_name,
                    "disabled": operation.user.disabled,
                    "_id": operation.user.id,
                    "email": operation.user.email,
                    "role_id": operation.user.role_id,
                    "work_location_ids": operation.user.work_location_ids,
                    "role": {
                        "name": operation.user.role.name,
                        "description": operation.user.role.description,
                        "_id": operation.user.role.id,
                    },
                    "work_locations": operation.user.work_locations  
                }
            } for operation in paginated_operations
        ],
        "pagination": {
            "page": page,
            "size": size,
            "total": paginated_operations.total,
            "has_more": paginated_operations.has_next
        }
    }

    return jsonify(response)

def create_operation():
    data = operation_parser.parse_args()

    # Create a new operation record
    new_operation = OperationModel(
        start_timestamp=data["start_timestamp"],
        complete_timestamp=data["complete_timestamp"],
        status=data['status'],  
        mark_status=data['mark_status'],  
        comment={
            "type": "string",  
            "comment": "string",
            "timestamp": data["complete_timestamp"] 
        },
        work_instruction_id=data['work_instruction_id'],  
        user_id=data["users_id"]  
    )
    new_operation.save()

    # Construct the response
    response = {
        "start_timestamp": data["start_timestamp"],
        "complete_timestamp": data["complete_timestamp"],
        "status": data["status"],
        "mark_status": data["mark_status"],
        "comment": data["comments"],
        "work_instruction_id": data["work_instruction_id"],
        "user_id": data["users_id"]
    }

    return jsonify(response)


def create_operation_comments():
    data = operation_parser.parse_args()

    # Create a new operation record
    new_operation = OperationModel( 
        comment = {
            "type": data['type'],  
            "comment": data['comment'], 
            "timestamp": data["comment"]
      }
    )
    new_operation.save()

    comment = {
        "type": data['type'],  
        "comment": data['comment'],  
        "timestamp": data['start_timestamp']
    }

    return jsonify(comment)


def update_operation(operation_id):  
    data = operation_parser.parse_args()  
    operation = OperationModel.get_by_id(operation_id)  
    
    if not operation:
        abort(404, message="Operation not found")
        
    operation.update(**data)
    
    # Construct the detailed response
    response = {
        "start_timestamp": operation.start_timestamp.isoformat(),  
        "complete_timestamp": operation.complete_timestamp.isoformat(),  
        "status": operation.status,
        "mark_status": operation.mark_status,
        "comment": {
            "type": operation.comment_type,
            "comment": operation.comment_text,
            "timestamp": operation.comment_timestamp.isoformat()
        },
        "_id": operation.id,
        "work_instruction_id": operation.work_instruction_id,
        "user_id": operation.user_id
    }
    
    return jsonify(response)

def agian_update_operation(operation_id):  
    data = operation_parser.parse_args()  
    operation = OperationModel.get_by_id(operation_id)  
    
    if not operation:
        abort(404, message="Operation not found")
        
    operation.update(**data)
    
    # Construct the detailed response
    response = {
        "start_timestamp": operation.start_timestamp.isoformat(),  
        "complete_timestamp": operation.complete_timestamp.isoformat(),  
        "status": operation.status,
        "mark_status": operation.mark_status,
        "comment": {
            "type": operation.comment_type,
            "comment": operation.comment_text,
            "timestamp": operation.comment_timestamp.isoformat()
        },
        "_id": operation.id,
        "work_instruction_id": operation.work_instruction_id,
        "user_id": operation.user_id
    }
    
    return jsonify(response)


def delete_operation(operation_id):  
    operation = OperationModel.get_by_id(operation_id)  

    if not operation:
        abort(404, message="Operation not found")
    
    operation.delete()
    return jsonify({'message': 'Operation deleted'})


def delete_all_operations():  
    operation_records = OperationModel.query.all()  
    for operation in operation_records:
        operation.delete()
    
    return jsonify({'message': 'All operations deleted'})
