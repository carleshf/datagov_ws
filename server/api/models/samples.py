#!/usr/bin/env python

from flask import request
from datetime import datetime

from server.run import db, app
from server.database.model import Sample, Issue

from server.api.formatter import *


def format_sample(reg):
	return {
		'id': reg.id,
		'name': reg.name,
		'path_variant': reg.path_variant,
		'path_annotation': reg.path_annotation,
		'sparse_matrix': reg.sparse_matrix,
		'dense_matrix': reg.dense_matrix,
		'es_index': reg.es_index,
		'issue_id': reg.issue_id,
	}


def validate_sample(reg):
	try:
		if 'id' in reg.keys():
			rid = reg['id']
		else:
			rid = -1
		valid = {
			'id': rid,
			'name': reg['name'],
			'path_variant': reg['path_variant'],
			'path_annotation': reg['path_annotation'],
			'sparse_matrix': reg['sparse_matrix'],
			'dense_matrix': reg['dense_matrix'],
			'es_index': reg['es_index'],
			'issue_id': reg['issue_id'],
			# issue
		}
		return (True, valid)
	except:
		return (False, {})



@app.route('/api/sample', methods = ['POST'])
@app.route('/api/sample/<int:rid>', methods = ['POST'])
def get_sample(rid = None):
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
			cnt = Sample.query.paginate(meta['pageNum'], meta['pageSize'], False)
			rst = [ format_sample(reg) for reg in cnt.items ]
			return ( return_result(rst, meta, cnt.total, ''), 200 )
		else:
			reg = Sample.query.filter_by(id = rid).first()
			if reg is None:
				return ( return_result([], meta, Sample.query.count(), 'No entries found with id "{}"'.format(rid)), 200 )
			else:
				return ( return_result(format_sample(reg), meta, Sample.query.count(), ''), 200 )
	except Exception as ex:
		return ( return_error(str(ex)), 500 )


@app.route('/api/sample', methods = ['PUT'])
@app.route('/api/sample/<int:rid>', methods = ['PUT'])
def put_sample(rid = None):
	try:
		body = request.get_json()
	except Exception as ex:
		return ( return_error('No body "Content-Type: application/json" was provided'), 400 )
	try:
		if body is None:
			return ( return_error('No body "Content-Type: application/json" was provided'), 400 )
		else:
			meta = get_meta(body)
			isValid, data = validate_sample(body)
			print(isValid, data, meta)
		
		if not isValid:
			return ( return_error('Invalid definition of object'), 400 )
		if rid is None: # This is a new sample
			iss = Issue.query.filter_by(id = data['issue_id']).first()
			if iss is None:
				return ( return_error('The content of the provided "issue_id" did not return any Issue'), 400 )
			new = Sample(name = data['name'], index = data['index'], issue = iss)
			db.session.add(new)
			db.session.commit()
			return ( return_result(format_sample(new), meta, Sample.query.count(), '', False), 200 )
		else: # This is an update
			old = Sample.query.filter_by(id = rid).all()
			if len(old) != 1:
				return ( return_error('More than one object found using id "{}"'.format(rid)), 400 )
			old = old[ 0 ]
			iss = Issue.query.filter_by(id = data['issue_id']).first()
			old.name = data['name']
			old.index = data['index']
			old.issue = iss
			db.session.commit()
			return ( return_result(format_sample(old), meta, Sample.query.count(), '', False), 200 )
	except Exception as ex:
		return ( return_error(str(ex)), 500 )