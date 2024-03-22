from flask_appbuilder import BaseView, expose
from airflow.plugins_manager import AirflowPlugin
from monitor_plugin.monitoring import get_cpu_usage, get_memory_usage
from flask import Blueprint

    
bp = Blueprint(
    "monitoring",
    __name__,
    template_folder="templates",  # registers airflow/plugins/templates as a Jinja template folder
    static_folder="static",
    static_url_path="/static/monitor_plugin",
)

class SystemMonitorView(BaseView):
    @expose('/')
    def list(self):
        cpu_usage = get_cpu_usage()
        memory_usage = get_memory_usage()
        return self.render_template(
            'system_monitor.html',
            cpu_usage=cpu_usage,
            memory_usage=memory_usage
        )
    

class SystemMonitorPlugin(AirflowPlugin):
    name = "system_monitor_plugin"
    operators = []
    flask_blueprints = [bp]
    hooks = []
    executors = []
    admin_views = [SystemMonitorView()]

    appbuilder_views = [{"name": "Monitoring", "category": "Plugins examples", "view": SystemMonitorView()}]


