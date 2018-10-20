from unittest import TestCase
import json

from app.api.v1 import app

class StoreManagerApp(TestCase):
  def setUp(self):
    self.client = app.test_client()
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
    self.existingUsers  = {
      "name": "Belio Dennis",
      "password": "belio",
      "email": "belio@gmail.com",
      "isStoreAttendant": "isStoreAttendant",
      "isAdmin": "isAdmin"
    }
    self.existingUserswithoutname = {
      "password": "belio",
      "email": "belio@gmail.com",
      "isStoreAttendant": "isStoreAttendant",
      "isAdmin": "isAdmin"
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


  def test_post_product(self):
    response = self.client.post(
      '/api/v1/products', data=json.dumps(self.products), headers={'Content-Type': 'application/json'})
    self.assertEqual(response.status_code, 201)

    bad_request_response = self.client.post(
      '/api/v1/products', headers={'Content-Type': 'application/json'})
    self.assertEqual(bad_request_response.status_code, 400)

    response_without_name = self.client.post(
      '/api/v1/products', data=json.dumps(self.productswithoutname), headers={'Content-Type': 'application/json'})
    self.assertEqual(response_without_name.status_code, 400)

    response_without_quantity = self.client.post(
      '/api/v1/products', data=json.dumps(self.productswithoutquantity), headers={'Content-Type': 'application/json'})
    self.assertEqual(response_without_quantity.status_code, 400)

    response_without_price = self.client.post(
      '/api/v1/products', data=json.dumps(self.productswithoutprice), headers={'Content-Type': 'application/json'})
    self.assertEqual(response_without_price.status_code, 400)

    response_without_attandant = self.client.post(
      '/api/v1/sales', data=json.dumps(self.saleswithoutattendant), headers={'Content-Type': 'application/json'})
    self.assertEqual(response_without_attandant.status_code, 400)

    response_without_office = self.client.post(
      '/api/v1/sales', data=json.dumps(self.saleswithoutoffice), headers={'Content-Type': 'application/json'})
    self.assertEqual(response_without_office.status_code, 400)

    response_without_price = self.client.post(
      '/api/v1/sales', data=json.dumps(self.saleswithoutprice), headers={'Content-Type': 'application/json'})
    self.assertEqual(response_without_price.status_code, 400)

  def test_view_all_products(self):
    response = self.client.get(
      '/api/v1/products', data=json.dumps(self.products), headers={'Content-Type':'application/json'})
    self.assertEqual(response.status_code, 200)

  def test_get_one_product(self):
    response = self.client.get(
      '/api/v1/products/1', data=json.dumps(self.products), headers={'Content-Type':'application/json'})
    self.assertEqual(response.status_code, 200)

  def test_get_sale(self):
    response = self.client.get(
      '/api/v1/sales', data=json.dumps(self.sales), headers={'Content-Type':'application/json'})
    self.assertEqual(response.status_code, 200)

  def test_get_one_sale(self):
    response = self.client.get(
      '/api/v1/sales/1', data=json.dumps(self.sales), headers={'Content-Type':'application/json'})
    self.assertEqual(response.status_code, 200)

  def test_post_sale(self):
    response = self.client.post(
      '/api/v1/sales', data=json.dumps(self.sales), headers={'Content-Type': 'application/json'})
    self.assertEqual(response.status_code, 201)

  def test_no_sale(self):
    response = self.client.get('/api/v1/sales/1')
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.get_data())
    self.assertEqual(data['message'], "specific product not found")