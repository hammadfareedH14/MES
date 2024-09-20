from flask import jsonify,request,current_app
from flask_restful import reqparse,abort
from models.upload import FileModel

upload_parser = reqparse.RequestParser()
upload_parser.add_argument(' filename', type=str, required=True, help="filename cannot be blank")
upload_parser.add_argument(' url ', type=str, required=True, help="url cannot be blank")


def get_upload_by_filename(upload_filename):
    upload = FileModel.get_by_filename(upload_filename)  

    if not upload:
        abort(404, description="Upload not found")

    response = {
        "url": upload.url,  
        "filename": upload.filename  
    }

    return jsonify(response)


def get_all_files():
    uploads = FileModel.query.all()

    response = {
        "items": [
            {
                "url": upload.url,  
                "filename": upload.filename  
            } for upload in uploads
        ]
    }
    return jsonify(response)


def upload_file():
    args = upload_parser.parse_args()

    newfile= FileModel(
    filename = args['filename'],
    file_url = args['url']
    )

    newfile.save()

    response = {
        "url": args['url'],          
        "filename": args['filename'] 
    }

    return jsonify(response), 201


def delete_files(upload_filename):
    upload = FileModel.get_by_filename(upload_filename)
    if not upload:
        abort(404, message="Upload not found")
    upload.delete()
    return jsonify({'message': 'Upload deleted'})


def delete_all_files():
    upload_records = FileModel.query.all()
    for upload in upload_records:
        upload.delete()
    return jsonify({'message': 'All uploads deleted'})
