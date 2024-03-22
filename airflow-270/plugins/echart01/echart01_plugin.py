from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint, jsonify, url_for
from flask_appbuilder import BaseView, expose

echarts_plugin_bp = Blueprint(
    'echarts_plugin_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/echart01'
)

class EChartsView(BaseView):
    route_base = "/echarts_plugin"
    default_view = "bar_chart"

    @expose("/")
    def bar_chart(self):
        return self.render_template("bar_chart.html")
    

@echarts_plugin_bp.route('/echarts/bar_chart', methods=['GET'])
def generate_bar_chart():
    data = {
        'categories': ['A', 'B', 'C', 'D', 'E'],
        'values': [23, 45, 56, 78, 90]
    }
    return jsonify(data)

def macros_utils():
    return 1


class EChartsPlugin(AirflowPlugin):
    name = "echarts_plugin"
    operators = []
    macros = [macros_utils]
    flask_blueprints = [echarts_plugin_bp]
    appbuilder_views = [{"name": "echart01", "category": "Plugins examples", "view": EChartsView()}]

