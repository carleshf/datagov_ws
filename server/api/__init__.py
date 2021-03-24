#!/usr/bin/env python

"""from .delete import *
from .get import *
from .put import *
from .update import *"""


from .project import ProjectAPI
"""
def add_fetchers(mount):
	mount.add_resource(ProjectAPI, '/datagov_ws_service/api/project/<int:pid>')
"""

from flask_restful import Resource
todos = {}

class TodoSimple(Resource):
	def get(self, todo_id):
		return {todo_id: todos[todo_id]}

	def put(self, todo_id):
		todos[todo_id] = request.form['data']
		return {todo_id: todos[todo_id]}

def add_fetchers(mount):
	mount.add_resource(TodoSimple, '/datagov_ws_service/api/<string:todo_id>')