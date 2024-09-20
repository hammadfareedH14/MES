from flask import request
from flask_restful import Resource
from helper_function.line import ( 
    get_line_by_id, 
    get_all_lines, 
    get_paginated_lines,
    create_line,
    update_line,
    delete_line
)  

class LineResource(Resource):
   
    def get(self, line_id=None):
        if line_id:
            return get_line_by_id(line_id)
        elif request.path == "/lines/all":
            return get_all_lines()
        else:
            return get_paginated_lines()
    def post(self):
        return create_line()

    def put(self, line_id):
        return update_line(line_id)

    def delete(self, line_id):
        return delete_line(line_id)
