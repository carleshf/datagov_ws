#!/usr/bin/env python

from flask import request
from datetime import datetime

from server.run import db, app
from server.database.model import Project, Issue

from server.api.formatter import *


def format_issue(reg):
	return {
		'id': reg.id,
		'acronym': reg.acronym,
		'url': reg.url,
		'comments': reg.comments,
		'completed': reg.completed,
		'completition': reg.completition,
		'project_id': reg.project_id,
		# samples
		# steps
	}


def validate_issue(reg):
	try:
		if 'id' in reg.keys():
			rid = reg['id']
		else:
			rid = -1
		valid = {
			'id': rid,
			'acronym': reg['acronym'],
			'url': reg['url'],
			'comments': reg['comments'],
			'completed': reg['completed'],
			'completition': None if reg['completition'] == '' else datetime.strptime(reg['completition']),
			'project_id': reg['project_id'],
			# samples
			# steps
		}
		return (True, valid)
	except:
		return (False, {})


@app.route('/api/issue', methods = ['POST'])
@app.route('/api/issue/<int:rid>', methods = ['POST'])
def get_issue(rid = None):
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
			cnt = Issue.query.paginate(meta['pageNum'], meta['pageSize'], False)
			rst = [ format_issue(reg) for reg in cnt.items ]
			return ( return_result(rst, meta, cnt.total, ''), 200 )
		else:
			reg = Issue.query.filter_by(id = rid).first()
			if reg is None:
				return ( return_result([], meta, Issue.query.count(), 'No entries found with id "{}"'.format(rid)), 200 )
			else:
				return ( return_result(format_issue(reg), meta, Issue.query.count(), ''), 200 )
	except Exception as ex:
		return ( return_error(str(ex)), 500 )


@app.route('/api/issue', methods = ['PUT'])
@app.route('/api/issue/<int:rid>', methods = ['PUT'])
def put_issue(rid = None):
	try:
		body = request.get_json()
	except Exception as ex:
		return ( return_error('No body "Content-Type: application/json" was provided'), 400 )
	try:
		if body is None:
			return ( return_error('No body "Content-Type: application/json" was provided'), 400 )
		else:
			meta = get_meta(body)
			isValid, data = validate_issue(body)
		
		if not isValid:
			return ( return_error('Invalid definition of object'), 400 )
		if rid is None: # This is a new issue
			proj = Project.query.filter_by(id = data['project_id']).first()
			if proj is None:
				return ( return_error('The content of the provided "project_id" did not return any Project'), 400 )
			new = Issue(acronym = data['acronym'], url = data['url'], comments = data['comments'], completed = data['completed'], completition = data['completition'], project = proj )
			db.session.add(new)
			db.session.commit()
			return ( return_result(format_issue(new), meta, Issue.query.count(), '', False), 200 )
		else: # This is an update
			old = Issue.query.filter_by(id = rid).all()
			if len(old) != 1:
				return ( return_error('More than one object found using id "{}"'.format(rid)), 400 )
			old = old[ 0 ]
			proj = Project.query.filter_by(id = data['project_id']).first()
			old.acronym = data['acronym']
			old.url = data['url']
			old.comments = data['comments']
			old.completed = data['completed']
			old.completition = data['completition']
			old.project = proj
			db.session.commit()
			return ( return_result(format_issue(old), meta, Issue.query.count(), '', False), 200 )
	except Exception as ex:
		return ( return_error(str(ex)), 500 )