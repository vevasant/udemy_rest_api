import os

from flask import Flask,jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from blacklist import BlackList

from resources.user import UserRegister,User,UserLogin,UserLogout
from resources.item import Item, ItemList
from resources.store import Store,StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['PROPAGATE_EXCEPTIONS']=True
app.config['JWT_BLACKLIST_ENABLED']=True
app.config['JWT_BLACKLIST_TOKEN_CHECKS']=['access','refresh']
app.secret_key = 'V33k5ha!' # define app.config['JWT_SECRET_KEY'], if app secret key needs to be different from JWT's
api = Api(app)


jwt = JWTManager(app) #/auth end point won't be created

@jwt.token_in_blacklist_loader
def check_if_in_blacklist(decrypted_token):
	return decrypted_token['jti'] in BlackList

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
	if identity == 1:
		is_admin = True
	else:
		is_admin = False
	return {'is_admin': is_admin }

@jwt.expired_token_loader
def expired_token_callback():
	return jsonify({
		'message':'The token has expired',
		'error': 'token_expired'
		}),401

@jwt.invalid_token_loader
def invalid_token_callback():
	return jsonify({
		'message':'The token is invalid',
		'error': 'token_invalid'
		}),401

@jwt.unauthorized_loader
def missing_token_callback():
	return jsonify({
		'message':'Need to have access token',
		'error': 'authorization required'
		}),401

@jwt.needs_fresh_token_loader
def fresh_token_callback():
	return jsonify({
		'message':'The token is not fresh',
		'error': 'fresh_token_required'
		}),401

@jwt.revoked_token_loader
def revoked_token_callback():
	return jsonify({
		'message':'The token has been revoled',
		'error': 'token_revoked'
		}),401

api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')
api.add_resource(UserRegister,'/register')
api.add_resource(User,'/user/<int:user_id>')
api.add_resource(UserLogin,'/login')
api.add_resource(UserLogout,'/logout')

if __name__=='__main__':
	from db import db
	db.init_app(app)
	app.run(port=5000,debug=True)