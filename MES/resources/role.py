from flask import request
from flask_restful import Resource
from helper_function.role import (  
    get_role_by_id, 
    get_all_roles, 
    get_paginated_roles, 
    create_role, 
    update_role, 
    delete_role,
    delete_all_roles
)

class RoleResource(Resource):  
    
    def get(self, role_id=None): 

        if role_id:
            return get_role_by_id(role_id)  
        elif request.path == "/roles/all":  
            return get_all_roles()  
        else:
            return get_paginated_roles()  

    def post(self):
        return create_role()  

    def put(self, role_id):  
        return update_role(role_id)  

    def delete(self, role_id=None): 
        if role_id:
            return delete_role(role_id)  
        elif request.path == "/roles/all":  
            return delete_all_roles()  
