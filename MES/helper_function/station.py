from flask import jsonify, abort
from models.station import StationModel
from flask_restful import reqparse,request

    # Initialize the parser
station_parser = reqparse.RequestParser()
station_parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
station_parser.add_argument('line_id', type=int, required=True, help="line_id cannot be blank!")

def get_station_by_id(station_id):
    station = StationModel.get_by_id(station_id)
    if not station:
        abort(404, description="Station not found")

    return jsonify({
        "name": station.name,
        "_id": station.id,
        "line_id": station.lines.id,
        "line": {
            "name": station.lines.name,
            "_id": station.lines.id,
            "shop_id": station.lines.shops.id,
            "shop": {
                "name": station.lines.shops.name,
                "_id": station.lines.shops.id
            }
        }
    })

def get_all_stations():
    stations = StationModel.query.all()
    response = {
        "items": [
            {
                "name": station.name,
                "_id": station.id,
                "line_id": station.lines.id,
                "line": {
                    "name": station.lines.name,
                    "_id": station.lines.id,
                    "shop_id": station.lines.shops.id,
                    "shop": {
                        "name": station.lines.shops.name,
                        "_id": station.lines.shops.id
                    }
                }
            } for station in stations
        ]
    }
    return jsonify(response)

def paginate_stations():
    page = request.args.get('page', 1)  
    per_page = request.args.get('per_page', 10) 
    paginated_stations = StationModel.query.paginate(page=page, per_page=per_page, error_out=False)
    response = {
        "items": [
            {
                "name": station.name,
                "_id": station.id,
                "line_id": station.lines.id,
                "line": {
                    "name": station.lines.name,
                    "_id": station.lines.id,
                    "shop_id": station.lines.shops.id,
                    "shop": {
                        "name": station.lines.shops.name,
                        "_id": station.lines.shops.id
                    }
                }
            } for station in paginated_stations.items
        ],
        "pagination": {
            "page": paginated_stations.page,
            "size": paginated_stations.per_page,
            "total": paginated_stations.total,
            "has_more": paginated_stations.has_next
        }
    }
    return jsonify(response)

def create_station():
    data = station_parser.parse_args()
    new_station = StationModel(name=data['name'], line_id=data['line_id'])
    new_station.save()
    return jsonify({'message': 'Station created', 'id': new_station.id})

def update_station(station_id):
    data = station_parser.parse_args()
    station = StationModel.get_by_id(station_id)
    if not station:
        abort(404, message="Station not found")
    station.update(**data)
    return jsonify({'message': 'Station updated', 'id': station.id})

def delete_station(station_id):
    station = StationModel.get_by_id(station_id)
    if not station:
        abort(404, message="Station not found")
    station.delete()
    return jsonify({'message': 'Station deleted'})
