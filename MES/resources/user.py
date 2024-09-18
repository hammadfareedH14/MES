from flask import request
from flask_restful import Resource
from helper_function.user import (  
    get_user_by_id, 
    get_all_users, 
    get_paginated_users, 
    get_current_user,
    create_user, 
    update_user, 
    delete_user,
    delete_all_users
)

class UserResource(Resource):  
    
    def get(self, user_id=None): 
        if user_id:
            return get_user_by_id(user_id)  
        elif request.path == "/users/all":  
            return get_all_users()
        elif request.path == "/current/users":  
            return get_current_user()
        else:
            return get_paginated_users()  

    def post(self):
        return create_user()  

    def put(self, user_id):  
        return update_user(user_id)  

    def delete(self, user_id=None): 
        if user_id:
            return delete_user(user_id)  
        elif request.path == "/users/all":  
            return delete_all_users()
