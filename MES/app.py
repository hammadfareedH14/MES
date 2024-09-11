from flask import Flask
from flask_restful import Api
from db import db
from resources.shop import ShopResource
from resources.line import LineResource
from resources.station import StationResource
from resources.location import LocationResource
from resources.route import RouteResource


app = Flask(__name__)
app.secret_key = 'hammad12@#$'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mes.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)

with app.app_context():
    db.create_all() 

# maps the endpoints
api.add_resource(ShopResource,'/shops/<int:shop_id>','/shops/all','/shops')
api.add_resource(LineResource,'/lines/<int:line_id>','/lines/all','/lines')
api.add_resource(StationResource, '/stations/<int:station_id>' ,'/station/all' ,'/stations') 
api.add_resource(LocationResource, '/locations/<int:location_id>' ,'/locations/all' ,'/locations',)
api.add_resource(RouteResource, '/routes/<int:route_id>' ,'/routes/all' ,'/routes') 


if __name__ == "__main__":
    app.run(port=4000, debug=True)