from flask_restful import Resource,reqparse
from models.store import StoreModel

class Store(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('name',
		type=str,
		required=True,
		help="This field can not be left empty")

	def get(self,name):
		store = StoreModel.find_by_name(name)
		if store:
			return store.json(),200
		else:
			return {'message','Store not found'},404

	def post(self,name):
		store = StoreModel.find_by_name(name)
		if store:
			return {'message':'Store with name {} already exists'.format(name)},400
		else:
			store = StoreModel(name)
			store.save_to_db()
			return store.json(),201

	def  delete(self,name):
		store = StoreModel.find_by_name(name)
		if store:
			store.delete()
			return {'message':'Item deleted'}
		else:
			return {'message':'Item not found'},404

class StoreList(Resource):

	def get(self):
		return {'stores': [ store.json() for store in StoreModel.query.all()]}


