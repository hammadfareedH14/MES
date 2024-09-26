from flask import jsonify, abort, request
from models.category import CategoryModel,Type
from flask_restful import reqparse

category_parser = reqparse.RequestParser()
category_parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
category_parser.add_argument('_type', type=str , required=True, help="_type cannot be blank!")


def get_category_by_id(category_id):
    category = CategoryModel.get_by_id(category_id)

    if not category:
        abort(404, message="Category not found")
    
    response = {
        "name": category.name,
        "_id": category.id,
        "type": category._type.value  
    }
    return jsonify(response)


def get_all_categories():
    categories = CategoryModel.query.all()

    response = {
        "items": [
            {
                "name": category.name,
                "_id":  category.id,
                "type": category._type.value
            } for category in categories
        ]
    }
    return jsonify(response)


def get_paginated_categories():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    paginated_categories = CategoryModel.query.paginate(page=page, per_page=per_page, error_out=False)

    response = {
        "items": [
            {
                "name": category.name,
                "_id": category.id,
                "type": category._type.value
            } for category in paginated_categories.items
        ],
        "pagination": {
            "page": paginated_categories.page,
            "size": paginated_categories.per_page,
            "total": paginated_categories.total,
            "has_more": paginated_categories.has_next
        }
    }
    return jsonify(response)

def get_types_categories(): 
    categories = CategoryModel.query.all()

    response = {
        "items": [
            {
                "name": category.name,
                "_id":  category.id,
                "type": category._type.value
            } for category in categories
        ]
    }
    return jsonify(response)


def create_category():
    data = category_parser.parse_args()

    category_type = Type[data['_type'].upper()]  
  
    new_category = CategoryModel(name=data['name'], _type=category_type)
    new_category.save()
    
    return jsonify({'message': 'Category created', 'id': new_category.id})



def update_category(category_id):
    data = category_parser.parse_args()
    category = CategoryModel.get_by_id(category_id)
    

    category.name = data['name']
    category._type = Type[data['_type'].upper()]  
    
  
    category.update()  

    return jsonify({'message': 'Category updated', 'id': category.id})



def delete_category(category_id):
    category = CategoryModel.get_by_id(category_id)
    if not category:
        abort(404, message="Category not found")
    category.delete()
    return jsonify({'message': 'Category deleted'})

def delete_all_categories():
    category_records = CategoryModel.query.all()  
    for category in category_records:
        category.delete()
    return jsonify({'message': 'All categories deleted'})
