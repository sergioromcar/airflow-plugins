from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint, jsonify, url_for
from flask_appbuilder import BaseView, expose
from macros01.utils import MyAirflowUtils


macros01_plugin_bp = Blueprint(
    'macros01_plugin_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/macros01'
)


def get_correlator(dag_run, task_instance):
    return MyAirflowUtils.get_correlator(dag_run, task_instance)


class Macros01Plugin(AirflowPlugin):
    name = "macros01_plugin"
    operators = []
    macros = [get_correlator]
    flask_blueprints = [macros01_plugin_bp]

