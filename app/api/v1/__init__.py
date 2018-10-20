# app/__init__.py

from flask_api import FlaskAPI

from config import app_config


def create_app():
  app= FlaskAPI(__name__,instance_relative_config=True)
  return app

app = create_app()

from app.api.v1 import views