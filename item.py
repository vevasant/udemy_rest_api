import sqlite3
from flask_restful import Resource,reqparse 
from flask_jwt import jwt_required

class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument("price",
		type=float,
		required=True,
		help="This field is required")

	@jwt_required()
	def get(self,name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM items WHERE name=?"
		result = cursor.execute(query,(name,))
		row = result.fetchone()

		if row:
			return {'name': row[0],'price': row[1]}, 200 
		return {"message": "Item not found"}, 404

	@classmethod
	def find_by_name(cls,name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = "SELECT * FROM items where name=?"
		result = cursor.execute(query,(name,))
		row = result.fetchone()
		connection.close()
		if row:
			return {'name': row[0],'price': row[1]}
		else:
			return None


	@classmethod 	
	def insert(cls,item):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = "INSERT INTO items VALUES (?,?)"
		cursor.execute(query,(item['name'],item['price']))
		connection.commit()
		connection.close()


	def post(self,name):
		if Item.find_by_name(name): 
			return {'message':'item with name {} already exists'.format(name)},400
		data = Item.parser.parse_args()
		new_item = {'name': name, 'price': data['price']}
		try:
			Item.insert(new_item)
		except:
			return {'message': 'Error occurred while inserting the item'}

		return new_item,201

	def delete(self,name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		
		query = "DELETE FROM items where name=?"
		cursor.execute(query,(name,))
		
		connection.commit()
		connection.close()

		return {'message': 'item deleted'}

	@classmethod
	def update(cls,item):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		
		query = "UPDATE items SET price=? WHERE name=?"
		cursor.execute(query,(item['price'],item['name']))
		
		connection.commit()
		connection.close()


	def put(self,name):
		data = Item.parser.parse_args()
		item = Item.find_by_name(name)
		updated_item = {'name':name,'price':data['price']}
		if  item is None:
			Item.insert(updated_item)
		else:
			Item.update(updated_item)
		return updated_item





class ItemList(Resource):
	def get(self):
		items = []
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		
		query = "SELECT * FROM items"
		result = cursor.execute(query)
		
		for row in result:
			item = {'name':row[0],'price':row[1]}
			items.append(item)

		connection.close()

		return {'items':items}