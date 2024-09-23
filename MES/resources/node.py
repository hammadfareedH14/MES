from flask import request
from flask_restful import Resource
from helper_function.node import (  
    get_node_by_id, 
    get_all_nodes, 
    get_paginated_nodes, 
    get_nodes_by_route_id,
    create_node, 
    update_node, 
    delete_node,
    delete_all_nodes
)

class NodeResource(Resource):  
    
    def get(self, node_id=None, route_id=None):
        if node_id:
            return get_node_by_id(node_id)
        elif route_id:
            return get_nodes_by_route_id(route_id)
        elif request.path == "/nodes/all":
            return get_all_nodes()
        elif request.path == '/nodes':
            return get_paginated_nodes()
        # else:
            # return get_paginated_nodes()


    def post(self):
        return create_node()  

    def put(self, node_id):  
        return update_node(node_id)  

    def delete(self, node_id=None): 
        if node_id:
            return delete_node(node_id)  
        elif request.path == "/nodes/all":  
            return delete_all_nodes()
