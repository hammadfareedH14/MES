from flask import request
from flask_restful import Resource
from helper_function.station import (
    get_station_by_id, 
    get_all_stations, 
    paginate_stations, 
    create_station, 
    update_station, 
    delete_station
)

class StationResource(Resource):


    def get(self, station_id=None):
        if station_id:
            return get_station_by_id(station_id)
        elif request.path == "/stations/all":
            return get_all_stations()
        else:
            return paginate_stations()

    def post(self):
        data = StationResource.parser.parse_args()
        return create_station(data)

    def put(self, station_id):
        return update_station(station_id)

    def delete(self, station_id):
        return delete_station(station_id)
