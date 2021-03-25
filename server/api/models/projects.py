#!/usr/bin/env python

from flask import request

from server.run import db, app
from server.database.model import Project

from server.api.formatter import *

def format_project(reg):
	return {
		'id': reg.id,
		'acronym': reg.acronym,
		'title': reg.title,
		'description': reg.description,
		'active': reg.active,
	}


def validate_project(reg):
	try:
		if 'id' in reg.keys():
			rid = reg['id']
		else:
			rid = -1
		valid = {
			'id': rid,
			'acronym': reg['acronym'],
			'title': reg['title'],
			'description': reg['description'],
			'active': reg['active']
		}
		return (True, valid)
	except:
		return (False, {})


@app.route('/api/project', methods = ['GET'])
@app.route('/api/project/<int:rid>', methods = ['GET'])
def get_project(rid = None):
	try:
		body = request.get_json()
	except Exception as ex:
		return ( return_error('No body "Content-Type: application/json" was provided'), 400 )
	try:
		if body is None:
			return ( return_error('No body "Content-Type: application/json" was provided'), 400 )
		else:
			meta = get_meta(body)
		if rid is None:
			cnt = Project.query.paginate(meta['pageNum'], meta['pageSize'], False)
			rst = [ format_project(reg) for reg in cnt.items ]
			return ( return_result(rst, meta, cnt.total, ''), 200 )
		else:
			reg = Project.query.filter_by(id = rid).first()
			if reg is None:
				return ( return_result([], meta, Project.query.count(), 'No entries found with id "{}"'.format(rid)), 200 )
			else:
				return ( return_result(format_project(reg), meta, Project.query.count(), ''), 200 )
	except Exception as ex:
		return ( return_error(str(ex)), 500 )


@app.route('/api/project', methods = ['PUT'])
@app.route('/api/project/<int:rid>', methods = ['PUT'])
def put_project(rid = None):
	try:
		body = request.get_json()
	except Exception as ex:
		return ( return_error('No body "Content-Type: application/json" was provided'), 400 )
	try:
		if body is None:
			return ( return_error('No body "Content-Type: application/json" was provided'), 400 )
		else:
			meta = get_meta(body)
			isValid, data = validate_project(body)
		
		if not isValid:
			return ( return_error('Invalid definition of object'), 400 )
		if rid is None: # This is a new project
			new = Project(acronym = data['acronym'], title = data['title'], description = data['description'], active = data['active'])
			db.session.add(new)
			db.session.commit()
			return ( return_result(format_project(new), meta, Project.query.count(), '', False), 200 )
		else: # This is an update
			old = Project.query.filter_by(id = rid).all()
			if len(old) != 1:
				return ( return_error('More than one object found using id "{}"'.format(rid)), 400 )
			old = old[ 0 ]
			old.acronym = data['acronym']
			old.title = data['title']
			old.description = data['description']
			old.active = data['active']
			db.session.commit()
			return ( return_result(format_project(old), meta, Project.query.count(), '', False), 200 )
	except Exception as ex:
		return ( return_error(str(ex)), 500 )