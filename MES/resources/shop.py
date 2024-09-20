from flask import request
from flask_restful import Resource
from helper_function.shop import (
    get_shop_by_id, 
    get_all_shops, 
    paginate_shops, 
    create_shop, 
    update_shop, 
    delete_shop
)

class ShopResource(Resource):
 
    def get(self, shop_id=None):
        if shop_id:
            return get_shop_by_id(shop_id)
        elif request.path == "/shops/all":
            return get_all_shops()
        else:
            return paginate_shops()

    def post(self):
        return create_shop()

    def put(self, shop_id):
        return update_shop(shop_id)

    def delete(self, shop_id):
        return delete_shop(shop_id)
