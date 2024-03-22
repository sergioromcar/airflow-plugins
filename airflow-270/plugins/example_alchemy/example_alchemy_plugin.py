from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint, jsonify, url_for
from airflow.www.views import AirflowModelView
from flask_appbuilder import BaseView, expose
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import  relationship
from flask_sqlalchemy.model import DefaultMeta
from airflow.security import permissions
from airflow.www.auth import has_access
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

db = SQLAlchemy()

example_alchemy_bp = Blueprint(
    'example_alchemy_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/example01'
)

class MyDataModel(db.Model):
    """
    Base class for model objects.
    """
    __table_args__ = {'schema': 'data'}
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
   
    def __repr__(self):
        return '<Users "{id}">'.format(id=self.id)
    

class Example01View(BaseView):
    route_base = "/example_alchemy_plugin"
    default_view = "data"

    @expose("/")
    def data(self):
        data = MyDataModel.query.limit(10).all()
        return self.render_template("data.html", data=data)


class Example01Plugin(AirflowPlugin):
    name = "example_alchemy"
    operators = []
    flask_blueprints = [example_alchemy_bp]
    appbuilder_views = [{"name": "example_alchemy", "category": "Plugins examples", "view": Example01View()}]

