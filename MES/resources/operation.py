from flask import request
from flask_restful import Resource
from helper_function.operation import (  
    get_operation_by_id,  
    get_all_operations,  
    get_paginated_operations,  
    create_operation, 
    create_operation_comments, 
    update_operation,
    delete_operation,  
    delete_all_operations  
)

class OperationResource(Resource):
    
    def get(self, operation_id=None):
        if operation_id:
            return get_operation_by_id(operation_id)  
        elif request.path == "/operation/all":
            return get_all_operations()  
        else:
            return get_paginated_operations()  

    def post(self,operation_id=None):
        if operation_id:
            return create_operation()  
        else:
            return create_operation_comments

    def put(self, node_id):
        return update_operation(node_id)  

    def delete(self, operation_id=None):
        if operation_id:
            return delete_operation(operation_id)  
        else:
            return delete_all_operations()  
