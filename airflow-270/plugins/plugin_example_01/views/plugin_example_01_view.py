from __future__ import annotations

from flask import (
    g,
    make_response,
    redirect,
    request,
    session as flask_session
)
from flask_appbuilder import expose
from flask_appbuilder.actions import action
from airflow.security import permissions
from airflow.www.views import AirflowModelView
from airflow.www.auth import has_access
from airflow.www import utils as wwwutil
from airflow.utils.session import provide_session
from plugin_example_01.models import plugin_example_01_model
from flask import Blueprint, jsonify, url_for
from flask_appbuilder import BaseView, expose
from markupsafe import Markup, escape
from airflow.www import auth, utils as wwwutils

import logging as log

class PluginExample01UsersView(AirflowModelView):
    """Creating a Flask-AppBuilder View"""
    
    route_base = '/plugin_example_01'

    datamodel = AirflowModelView.CustomSQLAInterface(plugin_example_01_model.PluginExample01UsersModel)
    base_permissions = [permissions.ACTION_CAN_EDIT, permissions.ACTION_CAN_DELETE, permissions.ACTION_CAN_READ, permissions.ACTION_CAN_ACCESS_MENU]

    label_columns = {
        'name': 'Name',
        'email': 'Email',
        'id': 'Link'
    }

    list_columns = ['id', 'name', 'email']
    search_columns = ['id', 'name', 'email']

    edit_columns = ['email']
    base_order = ('id', 'asc')

    list_template = 'plugin_example_01.html'
    list_title = "Users"


    def link(attr):
        id = attr.get('id')
        url = url_for(
            'PluginExample01UsersView.plugin_example_01_bar_chart',
            id=id)

        return Markup(
            '<a href="{}" ><i class="fa fa-bar-chart" style="color: orange;padding: 2px;font-size:20px"  title="{}"></i></a>'.format(
                url, id ))


    formatters_columns = {
        'id': link
    }


    @expose('/list/')
    @has_access([(permissions.ACTION_CAN_READ, permissions.RESOURCE_WEBSITE),(permissions.ACTION_CAN_READ, 'PluginExample01UsersView')])
    @provide_session
    def list(self,  session=None):
        widgets = self._list()
        return self.render_template(self.list_template,
                                    title=self.list_title,
                                    widgets=widgets)



    @expose('/public/')
    @provide_session
    def public(self,  session=None):
        widgets = self._list()
        return self.render_template(self.list_template,
                                    title=self.list_title,
                                    widgets=widgets)
    

    @expose("/plugin_example_01_bar_chart")
    def plugin_example_01_bar_chart(self):
        log.info("request.url views")
        log.info(request.url)
        user_id_filter = request.args.get('id')
        return self.render_template("plugin_example_01_bar_chart.html", id=user_id_filter)
    

    @action('muldelete', 'Delete', "Are you sure you want to delete selected records?",
            single=False)
    def action_muldelete(self, items):
        self.datamodel.delete_all(items)
        self.update_redirect()
        return redirect(self.get_redirect())

