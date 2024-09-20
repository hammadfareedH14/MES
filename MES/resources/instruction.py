from flask import request
from flask_restful import Resource
from helper_function.instruction import (  
    get_instruction_by_id, 
    get_all_instructions, 
    get_paginated_instruction, 
    create_instruction, 
    update_instruction, 
    delete_instruction,
    delete_all_instructions
)

class NodeResource(Resource):  
    
    def get(self, instruction_id=None): 
        if instruction_id:
            return get_instruction_by_id(instruction_id)  
        elif request.path == "/nodes/all":  
            return get_all_instructions()
        else:
            return get_paginated_instruction()  

    def post(self):
        return create_instruction()  

    def put(self, instruction_id):  
        return update_instruction(instruction_id)  

    def delete(self, instruction_id=None): 
        if instruction_id:
            return delete_instruction(instruction_id)  
        elif request.path == "/nodes/all":  
            return delete_all_instructions()
