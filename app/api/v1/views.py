from flask_api import FlaskAPI
from flask import jsonify, request
from datetime import datetime
import re

from . import app
from app.api.v1.models import Products, products, Sales, sales

@app.route('/', methods=['GET'])
def main():
  return 'This is main store manager'

@app.route('/api/v1/products', methods=['GET'])
def get_all_products():
  return jsonify({'products': products}), 200

@app.route('/api/v1/products/<int:_id>', methods=['GET'])
def get_one_product(_id):
  prod = [product for product in products if product['id'] == _id] or None
  if prod:
    return jsonify({'product': prod[0]})
  else:
    return jsonify({'message': "specific product not found"}), 200
  return jsonify({'message': "You have no product yet"}), 200

@app.route('/api/v1/products', methods=['POST'])
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
def get_one_sale(_id):
  sal = [sale for sale in sales if sale['id'] == _id] or None
  if sal:
    return jsonify({'sale': sal[0]}), 200
  else:
    return jsonify({'message': "specific product not found"}), 200

@app.route('/api/v1/sales', methods=['GET'])
def get_all_sales():
  return jsonify({'sales': sales}), 200

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    if request.json:
        if request.json.get('email'):
            if re.match(r"[A-Za-z0-9]+@[A-Za-z0-9]+.[A-Za-z0-9]", request.json.get('email')):
                if request.json.get('password'):
                    for user in existingUsers:
                        if user["email"] == request.json['email'].encode('utf-8') and user["password"] == request.json['password'].encode('utf-8'):
                            if loggedIn:
                                loggedIn[:] = []
                            loggedIn.append(user)
                            return jsonify({"message": "logged in successfully"}), 200
                        pass
                    return jsonify({"message": "invalid  credentials"}), 200
                return jsonify({"message": "please provide a password"}), 200
            return jsonify({"message": "Invalid email format"}), 200
        return jsonify({"message": "please provide an email"}), 200
    return jsonify({"message": "data must be json serialized"}), 200

@app.route('/api/v1/auth/signup', methods=['POST'])
def signup():
    if request.json:
        if request.json.get('email'):
            if re.match(r"[A-Za-z0-9]+@[A-Za-z0-9]+.[A-Za-z0-9]", request.json.get('email')):
                if request.json.get('password'):
                    if request.json.get('name'):
                        try:
                            if loggedIn[0]["isAdmin"]:
                                name = str(request.json.get('name'))
                                email = request.json.get('email').encode('utf-8')
                                password = request.json.get('password').encode('utf-8')
                                isStoreAttendant = request.json.get('isStoreAttendant')
                                isAdmin = request.json.get('isAdmin')
                                thisUser = Users(name=name, email=email, password=password, isStoreAttendant=isStoreAttendant, isAdmin=isAdmin)
                                thisUser.save()
                                return jsonify({"message": "User created successfully"})
                            return jsonify({"message": "Only admin can do that"}), 401
                        except IndexError:
                            return jsonify({"message": "no logged in user"})
                    return jsonify({"message": "please provide a name"}), 200
                return jsonify({"message": "please provide a password"}), 200
            return jsonify({"message": "Invalid email format"}), 200
        return jsonify({"message": "please provide an email"}), 200
    return jsonify({"message": "data must be json serialized"}), 400