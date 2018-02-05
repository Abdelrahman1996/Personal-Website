import sqlite3
from flask_restful import Resource, reqparse
from models.item import ItemModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
    
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('description',
        type=str,
        required=True,
        help="Every item needs a description"
    )
    parser.add_argument('image',
        type=str,
        required=True,
        help="Every item needs an image"
    )
    
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
           return {'items': [item.json()]}
        return {'message': 'item was not found'}
    
    @jwt_refresh_token_required
    def post(self, name):
        if ItemModel.find_by_name(name):
           return {"message": "Item with name {} already exists.".format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data['description'],data['image'])
        try:
          item.save_to_db()
        except:
           return {"message":"an error occurred when inserting the item."}, 500
        
        return item.json(), 201
    
    @jwt_refresh_token_required
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
           item.delete_from_db()
        return {"message": "item successfully deleted"}
    
    @jwt_refresh_token_required
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name, data['description'],data['image'])
        else:
            item.description = data['description']
            item.image = data['image']
        item.save_to_db()
        return item.json()
    
class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
