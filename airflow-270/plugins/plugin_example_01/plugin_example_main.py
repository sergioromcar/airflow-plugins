from airflow.plugins_manager import AirflowPlugin
from plugin_example_01.views import plugin_example_01_view
from flask import Blueprint, jsonify
from sqlalchemy import func


from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(metaclass=DefaultMeta)

from airflow.utils.session import provide_session
from plugin_example_01.models import plugin_example_01_model
from flask import request

# Configura el nivel de registro deseado
import logging as log
log.info("Este es un mensaje de registro")

bp = Blueprint(
    "plugin_example_01",
    __name__,
    template_folder="templates",  # registers airflow/plugins/templates as a Jinja template folder
    static_folder="static",
    static_url_path="/static/plugin_example_01",
)

@bp.route('/echarts/plugin_example_01_bar_chart', methods=['GET'])
@provide_session
def plugin_example_01_bar_chart(session=None):
    # Consulta para obtener los datos de la base de datos MySQL
    user_id_filter = request.args.get('id')

    # Si user_id_filter es None, asignamos el valor '-1'
    if user_id_filter is None:
        user_id_filter = '-1'
    
    # Consulta para obtener la media de llamadas para el usuario especificado
    query_result = session.query(
        plugin_example_01_model.PluginExample01TelecomDataModel.user_id,
        func.avg(plugin_example_01_model.PluginExample01TelecomDataModel.call_duration).label('avg_duration')
    ).filter(plugin_example_01_model.PluginExample01TelecomDataModel.user_id == user_id_filter).\
        group_by(plugin_example_01_model.PluginExample01TelecomDataModel.user_id).\
        limit(10).all()
    
    categories = []
    values = []

    for result in query_result:
        categories.append(result[0])
        values.append(result[1])

    data = {
        'categories': categories,
        'values': values
    }

    return jsonify(data)


class PluginExample01(AirflowPlugin):
    """Defining the plugin class"""

    name = "Plugin Example 01"
    flask_blueprints = [bp]
    appbuilder_views = [{"name": "plugin_example_01", "category": "Plugins examples", "view": plugin_example_01_view.PluginExample01UsersView()}]
