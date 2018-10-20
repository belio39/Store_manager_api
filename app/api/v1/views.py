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
  if request.json:
    if request.json.get('name'):
      if request.json.get('quantity'):
        if request.json.get('price'):
          if re.match(r"^[A-Za-z0-9]", request.json.get('name')):
            data = request.json
            name = data['name']
            quantity = data['quantity']
            price = data['price']
            date_posted = datetime.now()
            new_product = Products(name, quantity, price, date_posted)
            return jsonify({
              'message': 'success, Product created',
              'product': new_product.save()
            }), 201
          return jsonify({"message": "name should contain........"})
        return jsonify({"message": "product needs a price"}), 400
      return jsonify({"message": "product needs a quantity"}), 400
    return jsonify({"message": "product needs a name"}), 400
  return jsonify({"message": "bad request"}), 400

@app.route('/api/v1/sales', methods=['POST'])
@jwt_required
def create_sales():
  if request.json:
    if request.json.get('attendant'):
      if request.json.get('office'):
        if request.json.get('price'):
          if re.match(r"^[A-Za-z0-9]", request.json.get('attendant')):
            data = request.json
            attendant = data['attendant']
            office = data['office']
            price = data['price']
            date_posted = datetime.now()
            new_sale = Sales(attendant, office, price, date_posted)
            return jsonify({
              'message': 'success, Sale created',
              'sale': new_sale.save()
            }), 201
          return jsonify({"message": "name should contain........"})  
        return jsonify({"message": "sale needs a price"}), 400       
      return jsonify({"message": "sale needs office"}), 400   
    return jsonify({"message": "sale needs a attendant"}), 400        
  return jsonify({"message": "bad request"}), 400

@app.route('/api/v1/sales/<int:_id>', methods=['GET'])
@jwt_required
def get_one_sale(_id):
  sal = [sale for sale in sales if sale['id'] == _id] or None
  if sal:
    return jsonify({'sale': sal[0]}), 200
  else:
    return jsonify({'message': "specific product not found"}), 200

@app.route('/api/v1/sales', methods=['GET'])
@jwt_required
def get_all_sales():
  return jsonify({'sales': sales}), 200

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    if request.json:
        if request.json.get('email'):
            if re.match(r"[A-Za-z0-9]+@[A-Za-z0-9]+.[A-Za-z0-9]", request.json.get('email')):
                if request.json.get('password'):
                    for user in existingUsers:
                      print('print', request.json.get('email'))
                      print('existing', existingUsers)
                      if (user['email'] == request.json.get('email')) and (user['password'] == request.json.get('password')):
                        access_token = create_access_token(identity=user['email'])
                        return jsonify({"token": access_token, "message": "logged in successfully"}), 200
                    return jsonify({"message": "invalid  credentials"}), 400
                return jsonify({"message": "please provide a password"}), 400
            return jsonify({"message": "Invalid email format"}), 400
        return jsonify({"message": "please provide an email"}), 400
    return jsonify({"message": "data must be json serialized"}), 400

@app.route('/api/v1/auth/signup', methods=['POST'])
def signup():
    if request.json:
        if request.json.get('email'):
            if re.match(r"[A-Za-z0-9]+@[A-Za-z0-9]+.[A-Za-z0-9]", request.json.get('email')):
                if request.json.get('password'):
                    if request.json.get('name'):
                        try:
                            name = str(request.json.get('name'))
                            email = request.json.get('email')
                            password = request.json.get('password')
                            isStoreAttendant = request.json.get('isStoreAttendant')
                            isAdmin = request.json.get('isAdmin')
                            thisUser = User(name=name, email=email, password=password, isStoreAttendant=isStoreAttendant, isAdmin=isAdmin)
                            thisUser.save()
                            return jsonify({"message": "User created successfully"})
                        except IndexError:
                            return jsonify({"message": "no logged in user"})
                    return jsonify({"message": "please provide a name"}), 200
                return jsonify({"message": "please provide a password"}), 200
            return jsonify({"message": "Invalid email format"}), 200
        return jsonify({"message": "please provide an email"}), 200
    return jsonify({"message": "data must be json serialized"}), 400