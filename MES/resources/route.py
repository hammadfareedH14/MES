from flask_restful import Resource,request
from helper_function.route import (
    get_route_by_id, 
    get_all_routes, 
    get_paginated_routes,
    create_route, 
    update_route, 
    delete_route
)

class RouteResource(Resource):

    def get(self, route_id=None):
        if route_id:
            return get_route_by_id(route_id)
        elif request.path == "/routes/all":
            return get_all_routes()
        else:
            return get_paginated_routes()

    def post(self):
        return create_route()

    def put(self, route_id):
        return update_route(route_id,)

    def delete(self, route_id):
        return delete_route(route_id)
