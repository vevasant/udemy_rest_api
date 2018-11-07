from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required,jwt_optional,get_jwt_identity,fresh_jwt_required
from models.item import ItemModel

class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument("price",
		type=float,
		required=True,
		help="This field is required")

	parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store_id."
                        )

	@jwt_required
	def get(self,name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json(),200
		else:
			return {'message': 'Item not found'},404

	@fresh_jwt_required
	def post(self,name):
		if ItemModel.find_by_name(name): 
			return {'message':'item with name {} already exists'.format(name)},400
		data = Item.parser.parse_args()
		
		new_item = ItemModel(name,**data)
		try:
			new_item.save_to_db()
		except:
			return {'message': 'Error occurred while inserting the item'},500

		return new_item.json(),201

	def delete(self,name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()
			return {'message': 'item deleted'}
		return {'message': 'item not found'},404

	def put(self,name):
		data = Item.parser.parse_args()
		item = ItemModel.find_by_name(name)

		if item is None:
			item = ItemModel(name,**data)
		else:
			item.price = data['price']

		try:
			item.save_to_db()
		except:
			return {'message': 'Error occurred while inserting the item'},500
		
		return item.json()

class ItemList(Resource):

	@jwt_optional
	def get(self):
		user_id = get_jwt_identity()
		items = [item.json() for item in ItemModel.find_all()]
		if user_id:
			return { 'items': items},200
		else:
			return {
				'items' : [item['name'] for item in items],
				'message' : 'You need to login to get more details about items'
			},200
