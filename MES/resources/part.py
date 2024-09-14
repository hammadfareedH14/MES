from flask import request
from flask_restful import Resource
from helper_function.part import (  
    get_part_by_id, 
    get_all_parts, 
    get_paginated_parts, 
    create_part, 
    update_part, 
    delete_part,
    delete_all_parts
)

class PartResource(Resource):  
    
    def get(self, part_id=None): 

        if part_id:
            return get_part_by_id(part_id)  
        elif request.path == "/parts/all":  
            return get_all_parts()  
        else:
            return get_paginated_parts()  

    def post(self):
        return create_part()  

    def put(self, part_id):  
        return update_part(part_id)  

    def delete(self, part_id=None): 
        if part_id:
            return delete_part(part_id)  
        elif request.path == "/parts/all":  
            return delete_all_parts()  
