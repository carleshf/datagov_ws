#!/usr/bin/env python

from sqlalchemy import Table, Column, Integer, Boolean, String, DateTime, Time, ForeignKey
from sqlalchemy.orm import relationship

from server.run import db

class Project(db.Model):
	__tablename__ = 'projects'
	id = Column(Integer, primary_key = True)
	acronym = Column(String(100))
	title = Column(String(500))
	description = Column(String(2000))
	active = Column(Boolean)

	issue = relationship('Issue')

	def __str__(self):
		return '[project] {}'.format(self.title)

class Issue(db.Model):
	__tablename__ = 'issues'
	id = Column(Integer, primary_key = True)
	acronym = Column(String(100))
	url = Column(String(500))
	comments = Column(String(2500))
	completed = Column(Boolean, default = False)
	completition = Column(DateTime, nullable = True, default = None)

	project_id = Column(Integer, ForeignKey('projects.id'))
	project = relationship('Project', back_populates = 'issue')
	configuration_id = Column(Integer, ForeignKey('configurations.id'))
	configuration = relationship('Configuration', back_populates = 'issue')
	sample = relationship('Sample')
	step = relationship('Step')

	def __str__(self):
		return '[issue] {}'.format(self.acronym)

class Sample(db.Model):
	__tablename__ = 'samples'
	id = Column(Integer, primary_key = True)
	name = Column(db.String(100))
	path_variant = Column(db.String(500))
	path_annotation = Column(db.String(500))
	sparse_matrix = Column(db.String(1000))
	dense_matrix = Column(db.String(1000))
	es_index = Column(db.String(100))
	
	issue_id = Column(Integer, ForeignKey('issues.id'))
	issue = relationship('Issue', back_populates = 'sample')

class Step(db.Model):
	__tablename__ = 'steps'
	id = Column(Integer, primary_key = True)
	acronym = Column(String(100))
	title = Column(String(500))
	description = Column(String(2000))
	time = Column(Time)
	completed = Column(Boolean, default = False)
	completition = Column(DateTime, nullable = True, default = None)
	
	issue_id = Column(Integer, ForeignKey('issues.id'))
	issue = relationship('Issue', back_populates = 'step')


class Configuration(db.Model):
	__tablename__ = 'configurations'
	id = Column(Integer, primary_key = True)
	acronym = Column(String(100))
	url = Column(String(500))
	description = Column(String(2000))
		
	issue = relationship('Issue')