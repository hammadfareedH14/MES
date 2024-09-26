from flask import jsonify,request
from flask_restful import  reqparse,abort
from models.node import NodeModel

node_parser = reqparse.RequestParser()
node_parser.add_argument('current_station_id', type=str, required=True, help="current_station_id cannot be blank")
node_parser.add_argument('next_station_id', type=str, required=True, help="next_station_id cannot be blank")
node_parser.add_argument('is_start', type=bool, default=False, help="is_start is required")
node_parser.add_argument('is_end', type=bool, default=False, help="is_end is required")
node_parser.add_argument('route_id', type=str, required=True,help="route_id cannot be blank")


def get_node_by_id(node_id):
    node = NodeModel.get_by_id(node_id)

    if not node:
        abort(404, description="Node not found")

    response = {
        "timestamp": node.created_at,  
        "_id": node.id,
        "is_start": node.is_start,
        "is_end": node.is_end,
        "route_id": node.route_id,
        "current_station_id": node.current_station_id,
        "next_station_id": node.next_station_id,
        "route": {
            "name": node.routes.name,
            "description": node.routes.description,
            "_id": node.routes.id
        },
        "current_station": {
            "name": node.current_station.name,
            "_id": node.current_station.id,
            "line_id": node.current_station.line_id,
            "line": {
                "name": node.current_station.lines.name,
                "_id": node.current_station.lines.id,
                "shop_id": node.current_station.lines.shop_id,
                "shop": {
                    "name": node.current_station.lines.shops.name,
                    "_id": node.current_station.lines.shops.id
                }
            }
        },
        "next_station": {
            "name": node.next_station.name,
            "_id": node.next_station.id,
            "line_id": node.next_station.line_id,
            "line": {
                "name": node.next_station.lines.name,
                "_id": node.next_station.lines.id,
                "shop_id": node.next_station.lines.shop_id,
                "shop": {
                    "name": node.next_station.lines.shops.name,
                    "_id": node.next_station.lines.shops.id
                }
            }
        }
    }

    return jsonify(response)


def get_all_nodes():
    nodes = NodeModel.query.all()

    response = {
        "items": [
            {
                "timestamp": node.created_at,  
                "_id": node.id,
                "is_start": node.is_start,
                "is_end": node.is_end,
                "route_id": node.route_id,
                "current_station_id": node.current_station_id,
                "next_station_id": node.next_station_id
            } for node in nodes
        ]
    }
    return jsonify(response)


def get_paginated_nodes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    paginated_nodes = NodeModel.query.paginate(page=page, per_page=per_page, error_out=False)

    response = {
        "items": [
            {
                "timestamp": node.created_at,  
                "_id": node.id,
                "is_start": node.is_start,
                "is_end": node.is_end,
                "route_id": node.route_id,
                "current_station_id": node.current_station_id,
                "next_station_id": node.next_station_id,
                "route": {
                    "name": node.routes.name,
                    "description": node.routes.description,
                    "_id": node.routes.id
                },
                "current_station": {
                    "name": node.current_station.name,
                    "_id": node.current_station.id,
                    "line_id": node.current_station.line_id,
                    "line": {
                        "name": node.current_station.lines.name,
                        "_id": node.current_station.lines.id,
                        "shop_id": node.current_station.lines.shop_id,
                        "shop": {
                            "name": node.current_station.lines.shops.name,
                            "_id": node.current_station.lines.shops.id
                        }
                    }
                },
                "next_station": {
                    "name": node.next_station.name,
                    "_id": node.next_station.id,
                    "line_id": node.next_station.line_id,
                    "line": {
                        "name": node.next_station.lines.name,
                        "_id": node.next_station.lines.id,
                        "shop_id": node.next_station.lines.shop_id,
                        "shop": {
                            "name": node.next_station.lines.shops.name,
                            "_id": node.next_station.lines.shops.id
                        }
                    }
                }
            } for node in paginated_nodes.items
        ],
        "pagination": {
            "page": paginated_nodes.page,
            "size": paginated_nodes.per_page,
            "total": paginated_nodes.total,
            "has_more": paginated_nodes.has_next
        }
    }
    return jsonify(response)

def get_nodes_by_route_id(route_id): 
    nodes = NodeModel.query.filter_by(route_id=route_id).all()

    response = {
        "items": [
            {
                "timestamp": node.created_at,  
                "_id": node.id,
                "is_start": node.is_start,
                "is_end": node.is_end,
                "route_id": node.route_id,
                "current_station_id": node.current_station_id,
                "next_station_id": node.next_station_id,
                "route": {
                    "name": node.routes.name,
                    "description": node.routes.description,
                    "_id": node.routes.id
                },
                "current_station": {
                    "name": node.current_station.name,
                    "_id": node.current_station.id,
                    "line_id": node.current_station.line_id,
                    "line": {
                        "name": node.current_station.lines.name,
                        "_id": node.current_station.lines.id,
                        "shop_id": node.current_station.lines.shop_id,
                        "shop": {
                            "name": node.current_station.lines.shops.name,
                            "_id": node.current_station.lines.shops.id
                        }
                    }
                },
                "next_station": {
                    "name": node.next_station.name,
                    "_id": node.next_station.id,
                    "line_id": node.next_station.line_id,
                    "line": {
                        "name": node.next_station.lines.name,
                        "_id": node.next_station.lines.id,
                        "shop_id": node.next_station.lines.shop_id,
                        "shop": {
                            "name": node.next_station.lines.shops.name,
                            "_id": node.next_station.lines.shops.id
                        }
                    }
                }
            } for node in nodes
        ]
    }
    return jsonify(response)



def create_node():
    data = node_parser.parse_args()
    
    new_node = NodeModel(
        current_station_id=data['current_station_id'],
        next_station_id=data['next_station_id'],
        is_start=data['is_start'],
        is_end=data['is_end'],
        route_id=data['route_id']
    )
    new_node.save()

    response = {
        "timestamp": new_node.created_at,  
        "_id": new_node.id,
        "current_station_id": new_node.current_station_id,
        "next_station_id": new_node.next_station_id,
        "is_start": new_node.is_start,
        "is_end": new_node.is_end,
        "route_id": new_node.route_id
    }

    return jsonify(response)

def update_node(node_id):
    data = node_parser.parse_args()
    node = NodeModel.get_by_id(node_id)
    
    if not node:
        abort(404, description="Node not found")
        
    node.update(**data)
    
    response = {
        "timestamp": node.created_at,  
        "_id": node.id,
        "current_station_id": node.current_station_id,
        "next_station_id": node.next_station_id,
        "is_start": node.is_start,
        "is_end": node.is_end,
        "route_id": node.route_id
    }
    
    return jsonify(response)

def delete_node(node_id):
    node = NodeModel.get_by_id(node_id)
    if not node:
        abort(404, message="Node not found")
    node.delete()
    return jsonify({'message': 'Node deleted'})

def delete_all_nodes():
    node_records = NodeModel.query.all()
    for node in node_records:
        node.delete()
    return jsonify({'message': 'All nodes deleted'})
