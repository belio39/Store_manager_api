import unittest
import json

from app.api.v1 import app
from run import jwt

class StoreManagerApp(unittest.TestCase):
  def setUp(self):
    self.app = app
    self.client = self.app.test_client()
    self.products = {
      "name":"rtfhyuijk",
	    "quantity":"0",
	    "price":"0"
    }
    self.sales = {
      "attendant":"dennis",
      "office":"jogoo",
      "price":"123"
    }
    self.user  = {
      "name": "Belio Dennis",
      "password": "belio",
      "email": "belio@gmail.com",
    }

    self.productswithoutname = {
      "quantity":"0",
      "price":"0"
    }
    self.productswithoutquantity = {
      "price":"0"
    }
    self.productswithoutprice = {
      "":""
    }
    self.saleswithoutattendant = {
      "office":"jogoo",
      "price":"123"
    }
    self.saleswithoutoffice = {
      "price":"123"
    }

    self.saleswithoutprice = {
      "":""
    }

  def signup(self, data):
    response = self.client.post(
      '/api/v1/auth/signup', data=json.dumps(data),
      headers={'Content-Type': 'application/json'})
    return response

  def login(self, data):
    self.signup(self.user)
    response = self.client.post(
      '/api/v1/auth/login', data=json.dumps(data),
      headers={'Content-Type': 'application/json'})
    return response  

  def test_post_product(self):
    login = self.login(self.user)
    login_msg = json.loads(login.data)
    access_token = login_msg['access_token']
    response = self.client.post(
      '/api/v1/products', data=json.dumps(self.products),
      headers={'Authorization': 'Bearer {}'.format(access_token),
      'Content-Type': 'application/json'})  
    self.assertEqual(response.status_code, 201)

    bad_request_response = self.client.post(
      '/api/v1/products', headers={'Authorization': 'Bearer {}'.format(access_token),
      'Content-Type': 'application/json'})
    self.assertEqual(bad_request_response.status_code, 400)

    response_without_name = self.client.post(
      '/api/v1/products', data=json.dumps(self.productswithoutname),
      headers={'Authorization': 'Bearer {}'.format(access_token),
      'Content-Type': 'application/json'})  
    self.assertEqual(response_without_name.status_code, 400)

    response_without_quantity = self.client.post(
      '/api/v1/products', data=json.dumps(self.productswithoutquantity),
      headers={'Authorization': 'Bearer {}'.format(access_token),
      'Content-Type': 'application/json'})  
    self.assertEqual(response_without_quantity.status_code, 400)

    response_without_price = self.client.post(
      '/api/v1/products', data=json.dumps(self.productswithoutprice),
      headers={'Authorization': 'Bearer {}'.format(access_token),
      'Content-Type': 'application/json'})  
    self.assertEqual(response_without_price.status_code, 400)

    response_without_attandant = self.client.post(
      '/api/v1/sales', data=json.dumps(self.saleswithoutattendant),
      headers={'Authorization': 'Bearer {}'.format(access_token), 
      'Content-Type': 'application/json'})  
    self.assertEqual(response_without_attandant.status_code, 400)

    response_without_office = self.client.post(
      '/api/v1/sales', data=json.dumps(self.saleswithoutoffice),
      headers={'Authorization': 'Bearer {}'.format(access_token),
      'Content-Type': 'application/json'})  
    self.assertEqual(response_without_office.status_code, 400)

    response_without_price = self.client.post(
      '/api/v1/sales', data=json.dumps(self.saleswithoutprice),
      headers={'Authorization': 'Bearer {}'.format(access_token),
      'Content-Type': 'application/json'})  
    self.assertEqual(response_without_price.status_code, 400)

  def test_view_all_products(self):
    login = self.login(self.user)
    login_msg = json.loads(login.data)
    access_token = login_msg['access_token']
    response = self.client.get(
      '/api/v1/products', data=json.dumps(self.products),
      headers={'Authorization': 'Bearer {}'.format(access_token),
      'Content-Type': 'application/json'})  
    self.assertEqual(response.status_code, 200)

  def test_get_one_product(self):
    login = self.login(self.user)
    login_msg = json.loads(login.data)
    access_token = login_msg['access_token']
    self.client.post(
      '/api/v1/sales', data=json.dumps(self.products),
      headers={'Authorization': 'Bearer {}'.format(access_token),
      'Content-Type': 'application/json'})
    response = self.client.get(
      '/api/v1/products/1', data=json.dumps(self.products),
      headers={'Authorization': 'Bearer {}'.format(access_token),
      'Content-Type': 'application/json'})  
    self.assertEqual(response.status_code, 200)

  def test_get_sale(self):
    login = self.login(self.user)
    login_msg = json.loads(login.data)
    access_token = login_msg['access_token']
    response = self.client.get(
      '/api/v1/sales', data=json.dumps(self.sales),
      headers={'Authorization': 'Bearer {}'.format(access_token),
      'Content-Type': 'application/json'})  
    self.assertEqual(response.status_code, 200)

  def test_get_one_sale(self):
    login = self.login(self.user)
    login_msg = json.loads(login.data)
    access_token = login_msg['access_token']
    self.client.post(
      '/api/v1/sales', data=json.dumps(self.sales),
      headers={'Authorization': 'Bearer {}'.format(access_token),
      'Content-Type': 'application/json'})
    response = self.client.get(
      '/api/v1/sales/1', data=json.dumps(self.sales),
      headers={'Authorization': 'Bearer {}'.format(access_token),
      'Content-Type': 'application/json'})  
    self.assertEqual(response.status_code, 200)

  def test_post_sale(self):
    login = self.login(self.user)
    login_msg = json.loads(login.data)
    access_token = login_msg['access_token']
    response = self.client.post(
      '/api/v1/sales', data=json.dumps(self.sales),
      headers={'Authorization': 'Bearer {}'.format(access_token), 
      'Content-Type': 'application/json'})
    self.assertEqual(response.status_code, 201)

  def test_no_sale(self):
    login = self.login(self.user)
    login_msg = json.loads(login.data)
    access_token = login_msg['access_token']
    response = self.client.get('/api/v1/sales/1',
    data=json.dumps(self.sales), headers={'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'})
    self.assertEqual(response.status_code, 200)