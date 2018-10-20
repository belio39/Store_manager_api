import os
from flask_jwt_extended import JWTManager

from app.api.v1 import app

app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
jwt = JWTManager(app)


if __name__ == '__main__':

  app.run(debug=True)