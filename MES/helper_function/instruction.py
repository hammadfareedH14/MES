from flask import jsonify,request
from flask_restful import reqparse,abort
from models.instruction import InstructionModel

instruction_parser = reqparse.RequestParser()
instruction_parser.add_argument('current_station_id', type=str, required=True, help="current_station_id cannot be blank")
instruction_parser.add_argument('next_station_id', type=str, required=True, help="next_station_id cannot be blank")
instruction_parser.add_argument('is_start', type=bool, required=True, help="is_start is required")
instruction_parser.add_argument('is_end', type=bool, required=True, help="is_end is required")
instruction_parser.add_argument('route_id', type=str, required=True, help="route_id cannot be blank")


def get_instruction_by_id(instruction_id):
    instruction = InstructionModel.get_by_id(instruction_id)

    if not instruction:
        abort(404, message="Instruction not found")

    response = {
        "description": instruction.description,
        "_id": instruction.id,
        "category_id": instruction.category_id,
        "work_location_id": instruction.work_location_id,
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
            } for part in instruction.parts
        ],
        "category": {
            "name": instruction.category.name,
            "type": instruction.category._type.value,  
            "_id": instruction.category.id
        },
        "work_location": {
            "name": instruction.work_location.name,
            "_id": instruction.work_location.id,
            "station_id": instruction.work_location.station_id,
            "station": {
                "name": instruction.work_location.station.name,
                "_id": instruction.work_location.station.id,
                "line_id": instruction.work_location.station.line_id,
                "line": {
                    "name": instruction.work_location.station.line.name,
                    "_id": instruction.work_location.station.line.id,
                    "shop_id": instruction.work_location.station.line.shop_id,
                    "shop": {
                        "name": instruction.work_location.station.line.shop.name,
                        "_id": instruction.work_location.station.line.shop.id
                    }
                }
            }
        }
    }

    return jsonify(response)


def get_all_instructions():
    instructions = InstructionModel.query.all()

    response = {
        "items": [
            {
                "description": instruction.description,
                "_id": instruction.id,
                "category_id": instruction.category_id,
                "work_location_id": instruction.work_location_id,
                "parts": [
                    {
                        "part_id": part.id,
                        "image_url": part.image_url
                    } for part in instruction.parts
                ]
            } for instruction in instructions
        ]
    }
    return jsonify(response)


def get_paginated_instruction():
    page = int(request.args.get('page', 0))
    size = int(request.args.get('size', 10))

    instructions_query = InstructionModel.query.paginate(page=page, per_page=size, error_out=False)
    instructions = instructions_query.items
    
    response = {
        "items": [
            {
                "description": instruction.description,
                "_id": instruction.id,
                "category_id": instruction.category_id,
                "work_location_id": instruction.work_location_id,
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
                    } for part in instruction.parts
                ],
                "category": {
                    "name": instruction.category.name,
                    "type": instruction.category._type.value,
                    "_id": instruction.category.id
                },
                "work_location": {
                    "name": instruction.work_location.name,
                    "_id": instruction.work_location.id,
                    "station_id": instruction.work_location.station_id,
                    "station": {
                        "name": instruction.work_location.station.name,
                        "_id": instruction.work_location.station.id,
                        "line_id": instruction.work_location.station.line_id,
                        "line": {
                            "name": instruction.work_location.station.line.name,
                            "_id": instruction.work_location.station.line.id,
                            "shop_id": instruction.work_location.station.line.shop_id,
                            "shop": {
                                "name": instruction.work_location.station.line.shop.name,
                                "_id": instruction.work_location.station.line.shop.id
                            }
                        }
                    }
                }
            } for instruction in instructions
        ],
        "pagination": {
            "page": page,
            "size": size,
            "total": instructions_query.total,
            "has_more": instructions_query.has_next
        }
    }

    return jsonify(response)


def create_instruction():
    data = instruction_parser.parse_args()
    
    new_instruction = InstructionModel(
        current_station_id=data['current_station_id'],
        next_station_id=data['next_station_id'],
        is_start=data['is_start'],
        is_end=data['is_end'],
        route_id=data['route_id']
    )
    new_instruction.save()

    response = {
        "description": new_instruction.description,  
        "_id": new_instruction.id,  
        "category_id": new_instruction.category_id, 
        "work_location_id": new_instruction.work_location_id, 
        "parts": [
            {
                "part_id": part.id,  
                "image_url": part.image_url  
            } for part in new_instruction.parts  
        ]
    }

    return jsonify(response)


def update_instruction(instruction_id):
    data = instruction_parser.parse_args()
    instruction = InstructionModel.get_by_id(instruction_id)
    
    if not instruction:
        abort(404, message="Instruction not found")
        
    instruction.update(**data)
    
    response = {
        "name": instruction.name,
        "description": instruction.description,
    }
    
    return jsonify(response)



def delete_instruction(instruction_id):
    instruction = InstructionModel.get_by_id(instruction_id)

    if not instruction:
        abort(404, message="Instruction not found")
    
    instruction.delete()
    return jsonify({'message': 'Instruction deleted'})



def delete_all_instructions():
    instruction_records = InstructionModel.query.all()
    for instruction in instruction_records:
        instruction.delete()
    
    return jsonify({'message': 'All instructions deleted'})

