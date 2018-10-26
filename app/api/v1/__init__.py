# app/__init__.py

from flask_api import FlaskAPI


def create_app():
  """create app"""
  app = FlaskAPI(__name__, instance_relative_config=True)
  app.url_map.strict_slashes = False
  return app

app = create_app()

from . import views
