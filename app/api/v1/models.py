products = []
sales = []
existingUsers = []

class Products():

  def __init__(self, name, quantity, price, date_posted):
    self.name = name
    self.quantity = quantity
    self.price = price
    self.date_posted = date_posted

  def save(self):
    try:
      current_product = {
        "name": self.name,
        "quantity": self.quantity,
        "price": self.price,
        "date_posted": self.date_posted,
        "id": products[-1]['id']+1
      }

    except IndexError:
      current_product = {
        "name": self.name,
        "quantity": self.quantity,
        "price": self.price,
        "date_posted": self.date_posted,
        "id": 1
      }
    products.append(current_product)
    return current_product

class Sales():
  def __init__(self, attendant, office, price, date_posted):
    self.attendant = attendant
    self.office = office
    self.price = price
    self.date_posted = date_posted

  def save(self):
    try:
      current_sale = {
        "attendant": self.attendant,
        "office": self.office,
        "price": self.price,
        "date_posted": self.date_posted,
        "id": sales[-1]['id']+1
      }

    except IndexError:
      current_sale = {
        "attendant": self.attendant,
        "office": self.office,
        "price": self.price,
        "date_posted": self.date_posted,
        "id": 1
      }
    sales.append(current_sale)
    return current_sale
    

class User():
  def __init__(self, name, email, password, isAdmin=False, isStoreAttendant=False):
        self.name = name
        self.email = email
        self.password = password
        self.isAdmin = isAdmin
        self.isStoreAttendant = isStoreAttendant

  def save(self):
    currentUser = {
        "name": self.name,
        "password": self.password,
        "email": self.email,
        "isStoreAttendant": self.isStoreAttendant,
        "isAdmin": self.isAdmin,
    }
    existingUsers.append(currentUser)    