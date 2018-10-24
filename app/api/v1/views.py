from flask_api import FlaskAPI
from flask import jsonify, request
from datetime import datetime
import re
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from . import app
from app.api.v1.models import Products, products, Sales, sales, existingUsers, User

@app.route('/', methods=['GET'])
def main():
  return 'This is main store manager'

"""Provide a method to create access tokens. The create_access_token()"""

@app.route('/api/v1/products', methods=['GET'])
@jwt_required
def get_all_products():
  return jsonify({'products': products}), 200

@app.route('/api/v1/products/<int:_id>', methods=['GET'])
@jwt_required
def get_one_product(_id):
  prod = [product for product in products if product['id'] == _id] or None
  if prod:
    return jsonify({'product': prod[0]})
  else:
    return jsonify({'message': "specific product not found"}), 200
  return jsonify({'message': "You have no product yet"}), 200

@app.route('/api/v1/products', methods=['POST'])
@jwt_required
def create_products():
  data = request.json.get
  name = data('name')
  quantity = data('quantity')
  price = data('price')
  date_posted = datetime.now()
  if not name or not quantity or not price:
    return jsonify({'message': 'Name, quantity and price should not be empty.'}), 400
  if not name.isalnum():
    return jsonify({'message': 'Name contains only alphabets or numbers'}), 400
  new_product = Products(name, quantity, price, date_posted)
  return jsonify({
      'message': 'success, Product created',
      'product': new_product.save()
    }), 201

@app.route('/api/v1/sales', methods=['POST'])
@jwt_required
def create_sales():
  data = request.json.get
  attendant = data('attendant')
  office = data('office')
  price = data('price')
  date_posted = datetime.now()
  if not attendant or not office or not price:
    return jsonify({'message': 'Attendant, office and price should not be empty. '}), 400
  if not attendant.isalnum():
    return jsonify({'message': 'attendant contains only alphabets or numbers'}), 400
  new_sale = Sales(attendant, office, price, date_posted)
  return jsonify({
      'message': 'success, Sale created',
      'product': new_sale.save()
    }), 201  

@app.route('/api/v1/sales', methods=['GET'])
@jwt_required
def get_all_sales():
  return jsonify({'sales': sales}), 200

@app.route('/api/v1/sales/<int:_id>', methods=['GET'])
@jwt_required
def get_one_sale(_id):
  sal = [sale for sale in sales if sale['id'] == _id] or None
  if sal:
    return jsonify({'sale': sal[0]}), 200
  else:
    return jsonify({'message': "specific product not found"}), 200

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
  email = request.json.get('email')
  password = request.json.get('password')
  if not email or not password:
    return jsonify({'message': 'please provide email and password'}), 400
  if not re.match(r"[A-Za-z0-9]+@[A-Za-z0-9]+.[A-Za-z0-9]", email):
    return jsonify({"message": "Invalid email format"}), 400
  for user in existingUsers:
    if (user['email'] == request.json.get('email')) and (user['password'] == request.json.get('password')):
      access_token = create_access_token(identity=user['email'])
      return jsonify({"access_token": access_token, "message": "logged in successfully"}), 200
    return jsonify({"message": "invalid  credentials"}), 400

@app.route('/api/v1/auth/signup', methods=['POST'])
def signup():
  name = str(request.json.get('name'))
  email = request.json.get('email')
  password = request.json.get('password')
  isStoreAttendant = request.json.get('isStoreAttendant')
  isAdmin = request.json.get('isAdmin')
  if not email or not name or not password:
    return jsonify({'message': 'Please provide name, email and password'}), 400
  if not re.match("[A-Za-z0-9]+@[A-Za-z0-9]+.[A-Za-z0-9]", request.json.get('email')):
    return jsonify({"message": "Invalid email format"}), 400
  thisUser = User(name=name, email=email, password=password, isStoreAttendant=isStoreAttendant, isAdmin=isAdmin)
  thisUser.save()
  return jsonify({"message": "User created successfully"})