from flask import jsonify, abort
from models.shop import ShopModel
from flask_restful import reqparse,request


shop_parser = reqparse.RequestParser()
shop_parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")

def get_shop_by_id(shop_id):
    shop = ShopModel.get_by_id(shop_id)
    if not shop:
        abort(404, message="Shop not found")
    return jsonify({
        "name": shop.name,
        "_id": str(shop.id)
    })

def get_all_shops():
    shops = ShopModel.query.all()
    response = {
        "items": [
            {
                "name": shop.name,
                "_id": str(shop.id)
            } for shop in shops
        ]
    }
    return jsonify(response)

def paginate_shops(page, per_page):
    page = request.args.get('page', 1)  
    per_page = request.args.get('per_page', 10)  
    paginated_shops = ShopModel.query.paginate(page=page, per_page=per_page, error_out=False)
    response = {
        "items": [
            {
                "name": shop.name,
                "_id": str(shop.id)
            } for shop in paginated_shops.items
        ],
        "pagination": {
            "page": paginated_shops.page,
            "size": paginated_shops.per_page,
            "total": paginated_shops.total,
            "has_more": paginated_shops.has_next
        }
    }
    return jsonify(response)

def create_shop():
    data = shop_parser.parse_args()
    new_shop = ShopModel(name=data['name'])
    new_shop.save()
    return jsonify({'message': 'Shop created', 'id': new_shop.id})

def update_shop(shop_id, data):
    data = shop_parser.parse_args()
    shop = ShopModel.get_by_id(shop_id)
    if not shop:
        abort(404, message="Shop not found")
    shop.update(**data)
    return jsonify({'message': 'Shop updated', 'id': shop.id})

def delete_shop(shop_id):
    shop = ShopModel.get_by_id(shop_id)
    if not shop:
        abort(404, message="Shop not found")
    shop.delete()
    return jsonify({'message': 'Shop deleted'})
