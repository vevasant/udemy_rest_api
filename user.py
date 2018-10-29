import sqlite3
from flask_restful import Resource,reqparse

class User(object):
	def __init__(self,_id,username,password):
		self.id =_id
		self.username=username
		self.password=password

	@classmethod 
	def find_by_username(cls,username):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM users WHERE username=?"

		result = cursor.execute(query,(username,)).fetchone()

		connection.close()

		if result:
			user = cls(*result)
		else:
			user = None

		return user


	@classmethod
	def find_by_id(cls,_id):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM users WHERE id=?"

		result = cursor.execute(query,(_id,)).fetchone()

		connection.close()

		if result:
			user = cls(*result)
		else:
			user = None

		return user


class UserRegister(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('username',
		type=str,
		required=True,
		help="User Name has to be specified")
	parser.add_argument('password',
		type=str,
		required=True,
		help="Password has to be specified")

	def post(self):
		data = UserRegister.parser.parse_args()

		user = User.find_by_username(data['username'])

		if user is None:
			connection = sqlite3.connect('data.db')
			cursor = connection.cursor()
			
			query = "INSERT INTO users VALUES (NULL,?,?)"

			result = cursor.execute(query,(data['username'],data['password']))
			connection.commit()
			connection.close()
			return { "message" : "User created successfully"},201

		else:
			return { "message" : "User already exists" }, 400



