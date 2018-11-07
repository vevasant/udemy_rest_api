from flask_restful import Resource,reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
		create_access_token,
		create_refresh_token,
		jwt_required,
		get_jwt_claims,
		jwt_refresh_token_required,
		get_jwt_identity,
		get_raw_jwt
	)
from blacklist import BlackList



_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
		type=str,
		required=True,
		help="User Name has to be specified")
_user_parser.add_argument('password',
		type=str,
		required=True,
		help="Password has to be specified")

class UserRegister(Resource):

	def post(self):
		data = _user_parser.parse_args()

		user = UserModel.find_by_username(data['username'])

		if user is None:
			user = UserModel(**data)
			user.save_to_db()
			return { "message" : "User created successfully"},201

		else:
			return { "message" : "User already exists" }, 400

class User(Resource):

	def get(self,user_id):
		user = UserModel.find_by_id(user_id)
		if not user:
			return {'message': 'User not found'},404
		return user.json()

	@jwt_required
	def delete(self,user_id):
		claims = get_jwt_claims()
		if claims['is_admin'] == False:
			return {'message': 'You need to have admin priviledges'},401


		user = UserModel.find_by_id(user_id)
		if not user:
			return {'message':'User not found'},404
		user.delete_from_db()
		return {'message':'User deleted'}

class UserLogin(Resource):

	def post(self):

		data = _user_parser.parse_args()

		user = UserModel.find_by_username(data['username'])

		if user and safe_str_cmp(user.password,data['password']):
			access_token = create_access_token(identity=user.id, fresh=True)
			refresh_token = create_refresh_token(user.id)
			return { 
				'access_token': access_token, 
				'refresh_token': refresh_token
			}
		return {'message': 'Invalid  credentials'},401

class RefreshToken(Resource):

	@jwt_refresh_token_required
	def post(self):
		current_user_id = get_jwt_identity()
		access_token = create_access_token(identity=current_user_id,fresh=False)
		return {'access_token':access_token},200

class UserLogout(Resource):
	@jwt_required
	def post(self):
		jti = get_raw_jwt()['jti']
		BlackList.add(jti)
		return {'message': 'User logged out successfully'},200






