#!/usr/bin/env python

from flask_restful import Resource, marshal_with

from server.run import db
from server.database.model import *

def format_project(reg):
	return {
		'id': reg.id,
		'acronym': reg.acronym,
		'title': reg.title,
		'description': reg.description,
		'active': reg.active,
	}

def get(self, pid = None):
	if pid is None:
		try:
			cnt = Project.query().all()
			cnt = [ format_project(reg) for reg in cnt ]
			return ( { 'content': cnt }, 200 )
		except Exception as ex:
			return ( { 'content': str(ex) }, 400 )
	else:
		##TODO
		return ( { 'content': 'not implemented yet' }, 400 )

def put(self, data):
	try:
		if data['pid'] == -1:
			new = Project(acronym = data['acronym'], title = data['title'], description = data['description'], active = data['active'])
			db.session.add(new)
			db.session.commit()
			return ( 200, { 'content': { 'id': new.id } } )
		else:
			old = Project.query.filter_by(id = data['id'])
			if len(old) != 1:
				return { 'error': True, 'content': 'More than one object found using id "{}"'.format(data['id']) }
			old = old[ 0 ]
			old.acronym = data['acronym']
			old.title = data['title']
			old.description = data['description']
			old.active = data['active']
			db.session.commit()
			return { 'error': False, 'content': { 'id': old.id } }
	except Exception as ex:
		return ( 400,  { 'content': str(ex) } )