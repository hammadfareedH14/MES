from flask import request
from flask_restful import Resource
from helper_function.upload import ( 
    upload_file, 
    get_upload_by_filename, 
    get_all_files, 
    delete_files,
    delete_all_files
)

class UploadResource(Resource):  
    
    def get(self, upload_filename=None): 
        if upload_filename:
            return get_upload_by_filename(upload_filename) 
        else: 
            return get_all_files()

    def post(self):
        return upload_file()  
    
    def delete(self, upload_filename=None): 
        if upload_filename:
            return delete_files(upload_filename)  
        else:
            return delete_all_files()
