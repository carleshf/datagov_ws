#!/usr/bin/env python


# Default _meta values when none is provided
_default_meta_ = {
	'pageNum': 1,
	'pageSize': 20
}

# Validates the meta content when provided using default values
def validate_meta(meta):
	valid = {}
	meta_keys = meta.keys()
	if not 'pageNum' in meta_keys:
		valid['pageNum'] = _default_meta_['pageNum']
	else:
		valid['pageNum'] = meta['pageNum']
	if not 'pageSize' in meta_keys:
		valid['pageSize'] = _default_meta_['pageSize']
	else:
		if meta['pageSize'] > 0 and meta['pageSize'] < 1000:
			valid['pageSize'] = meta['pageSize']
		else:
			valid['pageSize'] = _default_meta_['pageSize']
	return valid

# Returns the _meta content of an incoming query
def get_meta(query):
	if '_meta' in query.keys():
		meta = validate_meta(query['_meta'])
	else:
		meta = _default_meta_
	return meta

# Function to format an error as standard return package
def return_error(msg):
	return {
		'data': { 'error': True, 'rst': [], 'des': msg },
		'_meta': _default_meta_
	}

# Function to format a result as standard return package
def return_result(rst, meta, total = -1, des = '', includeMeta = True):
	meta['totalItems'] = total
	if type(rst) is not list:
		rst = [ rst ]
	if includeMeta:
		return {
			'data': { 'error': False, 'rst': rst, 'des': des },
			'_meta': meta
		}
	else:
		return {
			'data': { 'error': False, 'rst': rst, 'des': des }
		}