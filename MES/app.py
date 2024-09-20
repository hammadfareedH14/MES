
from flask import Flask
from flask_restful import Api
from db import db
from resources.role import RoleResource
from resources.user import UserResource
from resources.shop import ShopResource
from resources.line import LineResource
from resources.station import StationResource
from resources.location import LocationResource
from resources.route import RouteResource
from resources.category import CategoryResource
from resources.part import PartResource
from resources.node import NodeResource
# from resources.upload import UploadResource
# from resources.instruction import InstructionResource
from resources.operation import OperationResource
from resources.datacapture import DataCaptureResource



app = Flask(__name__)
app.secret_key = 'hammad12@#$'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mes.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
api = Api(app)

with app.app_context():
    db.create_all() 

# maps the endpoints
api.add_resource(RoleResource, '/roles/<int:role_id>' ,'/roles/all' ,"/roles/types",'/roles') 
api.add_resource(UserResource, '/users/<int:user_id>' ,'/users/all' ,'/users',"/current/users") 
api.add_resource(ShopResource,'/shops/<int:shop_id>','/shops/all','/shops')
api.add_resource(LineResource,'/lines/<int:line_id>','/lines/all','/lines')
api.add_resource(StationResource, '/stations/<int:station_id>' ,'/station/all' ,'/stations') 
api.add_resource(LocationResource, '/locations/<int:location_id>' ,'/locations/all' ,'/locations',)
api.add_resource(RouteResource, '/routes/<int:route_id>' ,'/routes/all' ,'/routes') 
api.add_resource(CategoryResource, '/categories/<int:category_id>' ,'/categories/all' ,"/Categories/types",'/categories') 
api.add_resource(PartResource, '/parts/<int:part_id>' ,'/part/all' ,"/parts/types",'/parts')
api.add_resource(NodeResource, '/nodes/<int:node_id>' ,'/nodes/all' ,'/nodes',"/nodes/by_route") 
# api.add_resource(InstructionResource, '/nodes/<int:node_id>' ,'/nodes/all' ,'/nodes',"/nodes/by_route_id")
# api.add_resource(UploadResource, '/uploads/<str:upload_filename>' ,'/uploads/all', ) 
# api.add_resource(OperationResource, '/operations/<int:operation_id>' ,'/operations/all' ,'/operations') 
# api.add_resource(DataCaptureResource, '/datacaptures/<int:datacapture_id>' ,'/datacaptures/all' ,'/datacaptures') 


 

if __name__ == "__main__":
    app.run(port=4000, debug=True)
