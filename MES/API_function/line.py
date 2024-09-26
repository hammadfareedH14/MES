from flask import jsonify,request
from flask_restful import  abort, reqparse
from models.line import LineModel  
# from models.shop import ShopModel

line_parser = reqparse.RequestParser() # initilize parser
line_parser.add_argument('name', type=str, required=True, help="Name cannot be blank!") 
line_parser.add_argument('shop_id', type=int, required=True, help="shop_id cannot be blank!")  

# Function to retrieve line by ID
def get_line_by_id(line_id):
        line = LineModel.get_by_id(line_id)
        if not line:
            abort(404, message="Line not found")

        # shop_record = ShopModel.get_by_id()

        return jsonify({
            "name": line.name,
            "_id": line.id,
            "shop_id": line.shops.id,
            "shop": {
                "name": line.shops.name,
                "_id": line.shops.id
            } 
        })

# Function to retrieve all lines
def get_all_lines():
        lines = LineModel.query.all()

        response = {
            "items": [
                {
                    "name": line.name,
                    "_id": line.id,
                    "shop_id": line.shops.id,
                    "shop": {
                        "name": line.shops.name,
                        "_id": line.shops.id
                    }
                } for line in lines
            ]
        }
        return jsonify(response)

# Function to paginate lines
def get_paginated_lines():
        page =  request.args.get('page', 1) 
        per_page = request.args.get('per_page', 10)  

        paginated_lines = LineModel.query.paginate(page=page, per_page=per_page, error_out=False)

        response = {
            "items": [
                {
                    "name": line.name,
                    "_id": line.id,
                    "shop_id": line.shops.id,
                    "shop": {
                        "name": line.shops.name,
                        "_id": line.shops.id
                    }
                } for line in paginated_lines.items
            ],
            "pagination": {
                "page": paginated_lines.page,
                "size": paginated_lines.per_page,
                "total": paginated_lines.total,
                "has_more": paginated_lines.has_next 
            }
        }

        return jsonify(response)


def create_line():
        data = line_parser.parse_args()
        new_line = LineModel(name=data['name'], shop_id=data['shop_id'])
        new_line.save()
        return jsonify({'message': 'Line created', 'id': new_line.id})

def update_line(line_id):
        data = line_parser.parse_args()
        line = LineModel.get_by_id(line_id)
        if not line:
            abort(404, message="Line not found")
        line.update(**data)
        return jsonify({'message': 'Line updated', 'id': line.id})

def delete_line(line_id):
        line = LineModel.get_by_id(line_id)
        if not line:
            abort(404, message="Line not found")
        line.delete()
        return jsonify({'message': 'Line deleted'})
