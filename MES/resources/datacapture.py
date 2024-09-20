from flask import request
from flask_restful import Resource
from helper_function.datacapture import (  
    get_datacapture_by_id,  
    get_all_datacaptures,  
    get_paginated_datacaptures,  
    create_datacapture, 
    update_datacapture,
    delete_datacapture,  
    delete_all_datacaptures  
)

class DataCaptureResource(Resource):
    
    def get(self, datacapture_id=None):
        if datacapture_id:
            return get_datacapture_by_id(datacapture_id)  
        elif request.path == "/datacapture/all":
            return get_all_datacaptures()  
        else:
            return get_paginated_datacaptures()  

    def post(self):
            return create_datacapture()  

    def put(self, datacapture_id):
        return update_datacapture(datacapture_id)  

    def delete(self, datacapture_id=None):
        if datacapture_id:
            return delete_datacapture(datacapture_id)  
        else:
            return delete_all_datacaptures()
