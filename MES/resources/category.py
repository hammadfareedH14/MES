from flask import request, jsonify
from flask_restful import Resource
from helper_function.category import (
    get_category_by_id, 
    get_all_categories, 
    get_paginated_categories, 
    create_category, 
    update_category, 
    delete_category,
    delete_all_categories,
    get_types_categories
)

class CategoryResource(Resource):

    def get(self, category_id=None):
        if category_id:
            return get_category_by_id(category_id)
        elif request.path == "/categories/all":
            return get_all_categories()
        elif request.path == "/categories/types": 
            return get_types_categories()
        else:
            return get_paginated_categories()

    def post(self):
        return create_category()

    def put(self, category_id):
        return update_category(category_id)

    def delete(self, category_id=None):
        if category_id:
            return delete_category(category_id)
        else:
            return delete_all_categories()
        
