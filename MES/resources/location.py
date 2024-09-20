from flask_restful import Resource, request
from helper_function.location import (
    get_location_by_id,
    get_all_locations,
    get_paginated_locations,
    create_location,
    update_location,
    delete_location,
    delete_all_location
)

class LocationResource(Resource):

    def get(self, location_id=None):
        if location_id:
            return get_location_by_id(location_id)
        elif request.path == "/locations/all":
            return get_all_locations()
        else:
            args = LocationResource.pagination_parser.parse_args()
            return get_paginated_locations(args)

    def post(self):
        return create_location()

    def put(self, location_id):
        return update_location(location_id)

    def delete(self, location_id):
            return delete_location(location_id)
        