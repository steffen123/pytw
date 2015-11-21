# -*- coding: utf8 -*-

# Copyright (C) 2014-2015 Steffen Schaumburg and contributors, see docs/contributors.txt <steffen@schaumburger.info>
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
# In the original distribution you can find the license in docs/agpl_3.0.txt.

#TODO add controllable auto-commit
#TODO make all methods None-safe
#TODO make it SQL injection and whatnot safe, wtf is wrong with me

#python std lib
from datetime import date, datetime
import subprocess

#other 3rd party libs
#from typing import Any, Dict, List

#PyQt modules
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

#own modules
from .messenger import Messenger

class SQLFeeder():
	def __init__(self, messenger: Messenger, backend: str, db_name: str) -> None:
		#print("connecting to DB %s" % db_name)
		self.messenger = messenger
		self.backend = backend
		
		if backend == 'PGSQL':
			self.database = QSqlDatabase.addDatabase("QPSQL7", db_name) #TODO find out if I want QPSQL or QPSQL7
			self.database.setHostName("localhost")
			self.database.setDatabaseName(db_name)
			self.database.setUserName("postgres")
			#self.database.setPassword("")
		elif backend == 'SQLITE':
			self.database = QSqlDatabase.addDatabase("QSQLITE", db_name)
			self.database.setDatabaseName('%s.sqlite3' % db_name)
		else:
			self.messenger.message_fatal("invalid DB backend: %s" % backend)
		
		connected = False
		ok = self.database.open()
		if not ok:
			self.messenger.message_fatal("DB open error:" + self.database.lastError().text())
		else:
			self.cursor = QSqlQuery(self.database)
			ok = self.cursor.exec_()
			#self.execute('SET time_zone = "+00:00";')
			self.messenger.message_debug("Connected to DB %s" % db_name)
			connected = True
		
		#self.execute("SET time_zone = 'Europe/Berlin'")
	
	def _attach_params(self, param_dict) -> None:
		for key, value in param_dict.items():
			if type(value) == datetime: #TODO: time
				self.cursor.bindValue(':'+key, value.strftime('%Y-%m-%d %H:%M:%S'))
			elif type(value) == date:
				self.cursor.bindValue(':'+key, value.strftime('%Y-%m-%d') + " 00:00:00")
			else:
				self.cursor.bindValue(':'+key, value)
			
			#if key == 'stackable':
			#	print(value)
	
	def _attach_where_params(self, where_param_dicts) -> None: #TODO pretty sure this is an *exact* dupe of _attach_params
		if where_param_dicts:
			for key, comparator, value in where_param_dicts:
				if type(value) == datetime: #TODO: time
					self.cursor.bindValue(':'+key, value.strftime('%Y-%m-%d %H:%M:%S'))
				elif type(value) == date:
					self.cursor.bindValue(':'+key, value.strftime('%Y-%m-%d') + " 00:00:00")
				else:
					self.cursor.bindValue(':'+key, value)
	
	#def create_table(self, name: str, comment: str, dict_list: List[Dict[str,str]], debug=False) -> None:
	def create_table(self, name: str, comment: str, dict_list, debug=False) -> None:
		id_found = False
		for dict_to_check in dict_list:
			if dict_to_check['name'] == 'id':
				id_found = True
				break
		
		if not id_found:
			dict_list = ({'not_null':True, 'name':'id', 'type':'PKEY'}, ) + dict_list
		
		field_part = ''
		dict_list += ({'not_null':True, 'name':'row_created_ts', 'type':'DATETIME', 'default':'NOW()'},
				{'not_null':True, 'name':'row_modified_ts', 'type':'DATETIME', 'default':'NOW()'})
		
		if len(dict_list) > 0:
			for field in dict_list:
				if field['type'] == 'PKEY':
					if self.backend == 'SQLITE':
						field_type = 'INTEGER PRIMARY KEY'
					else:
						field_type = 'BIGSERIAL, PRIMARY KEY (%s)' % field['name']
				elif field['type'] == 'FKEY':
					if self.backend == 'SQLITE':
						field_type = 'INTEGER REFERENCES %s(id)' % field['fkey_table']
					else:
						if field['not_null']:#TODO unite with normal not_null code
							not_null = ' NOT NULL'
						else:
							not_null = ''
						
						if 'default' in field: #TODO unite with normal default code and add to sqlite, this probably fixes TabHave
							default = "DEFAULT '%s'" % field['default']
						else:
							default = ''
						field_type = 'BIGINT%s, FOREIGN KEY (%s) REFERENCES %s(id)' % (not_null, field['name'], field['fkey_table'])
				elif field['type'].startswith('ENUM'):
					if self.backend == 'SQLITE':
						field_type = 'TEXT'
						self.messenger.message_debug("SQLite doesnt know data type ENUM, setting TEXT instead")
					else:
						self._execute('DROP TYPE', 'DROP TYPE IF EXISTS %s_enum CASCADE' % (field['name']), True) #TODO convert to method
						self._execute('CREATE TYPE', 'CREATE TYPE %s_enum AS %s' % (field['name'], field['type']), True) #TODO convert to method
						field_type = '%s_enum' % field['name']
				elif field['type'].startswith('VARCHAR') or field['type'].startswith('CHAR'):
					if self.backend == 'SQLITE':
						field_type = 'TEXT'
					else:
						field_type = field['type']
				elif field['type'] == 'DATETIME':
					if self.backend == 'SQLITE':
						pass
					else:
						field_type = 'TIMESTAMP'
				else:
					if field['type']:
						if self.backend == 'PGSQL' and field['type'] == 'INT16': #TODO move into one layer up in the code structure
							field_type = 'INT2'
						elif self.backend == 'PGSQL' and field['type'] == 'INT32':
							field_type = 'INT4'
						elif self.backend == 'PGSQL' and field['type'] == 'INT64':
							field_type = 'INT8'
						elif self.backend == 'SQLITE' and field['type'] in ('INT16', 'INT32', 'INT64'):
							field_type = 'INTEGER'
						else:
							field_type = field['type']
					else:
						print("empty type for", field) #TODO better warning
				
				if field['not_null'] and field['type'] != 'PKEY' and field['type'] != 'FKEY': #PKEYs don't have this explicitly, fkey does it further above
					not_null = ' NOT NULL'
				else:
					not_null = ''
				
				if 'default' in field and field['type'] != 'FKEY': #fkey sets this further above
					default = " DEFAULT '%s'" % field['default']
				else:
					default = ''
				
				field_part += '  %s %s%s%s,\n' % (field['name'], field_type, not_null, default)
		else:
			print('Need to have params for create_table. Called it with:', name, dict_list, debug)
			return
		query = 'CREATE TABLE %s (\n%s\n)' % (name, field_part[:-2])
		if self.backend == 'PGSQL':
			self._execute('DROP TABLE', 'DROP TABLE IF EXISTS %s CASCADE' % name, debug) #TODO move into separate method
		else:
			self._execute('DROP TABLE', 'DROP TABLE IF EXISTS %s' % name, debug) #TODO move into separate method
		self._execute('CREATE TABLE', query, debug)
		
		#TODO comment on table and on rows
	
	def _execute(self, operation: str, query: str, debug: bool) -> None:
		if debug:
			print('exec:', query) #TODO restore this functionality: 'with params:', param_dict, "where", where_param_dict, "\n")
		
		if operation in ('CREATE TABLE', 'CREATE TYPE', 'DROP TABLE', 'DROP TYPE', '\dt', 'JUST RUN IT'):
			ok = self.cursor.exec_(query)
		else:
			ok = self.cursor.exec_()
		
		if not ok:
			print("sql error on execute:", self.cursor.lastError().text())
			print("    on this query:", self.cursor.lastQuery())
			raise Exception("invalid vals in db.execute_safe\n")
	
	def export(self, path: str) -> None: #TODO improve
		#print("started export")
		proc = subprocess.call(['./pg_dumper.sh', path])
		if proc != 0:
			self.messenger.message_warning(self, "Error trying to dump DB")
		print("done export")
	
	#def _fetch(self, param_list: List[str]) -> List[Dict[str,Any]]:
	def _fetch(self, param_list):
		result = []
		#print('fetch start')
		while self.next():
			row = {}
			counter = 0
			for key in param_list:
				row[key] = self.value(counter)
				#print(row[key])
				counter += 1
			result.append(row)
		#print('fetch end')
		
		return result
	
	def insert(self, table: str, param_dict, debug=False) -> None:
		into_part = ''
		values_part = ''
		if len(param_dict) > 0:
			for key in param_dict.keys():
				into_part += key + ', '
				values_part += ':' + key + ', '
			into_part = into_part[:-2]
			values_part = values_part[:-2]
		else:
			print('Need to have params for insert. Called it with:', table, param_dict, debug)
			return
		query = 'INSERT INTO %s (%s) VALUES(%s)' % (table, into_part, values_part)
		self._prepare(query)
		self._attach_params(param_dict)
		self._execute('INSERT', query, debug)
	
	def last_insert_id(self) -> int:
		return self.cursor.lastInsertId()
	
	def next(self) -> bool: #TODO check return type in API doc
		return self.cursor.next() #TODO error handling
	
	def _prepare(self, query: str) -> None:
		if not self.cursor.prepare(query):
			print("sql error on prepare:", self.cursor.lastError().text())
			print("    on this query:", self.cursor.lastQuery())
	
	#def select(self, table: str, param_list: List[str], where_param_dicts: List[Dict[str,Any]], where_literal="", debug=False) -> List[Dict[str,Any]]: #TODO limit
	def select(self, table: str, param_list, where_param_dicts=[], where_literal="", debug=False): #TODO limit
		#print("where_param_dicts", where_param_dicts)
		field_list = ''
		if len(param_list) > 0:
			for key in param_list:
				field_list += key + ', '
			field_list = field_list[:-2]
			
			where_part = '' #TODO move into separate method and convert other method to use that
			if not where_param_dicts:
				where_part = None
			elif len(where_param_dicts) == 0:
				where_part = None 
			else:
				for param_dict in where_param_dicts: #TODO apply this to all other methods, or better, unify code
					if type(param_dict['value']) == str:
						param_dict['value'] = param_dict['value'].replace("'", "") #TODO remove once i attach params properly
						if self.backend == 'SQLITE':
							param_dict['value'] = '"' + param_dict['value'] + '"'
						else:
							param_dict['value'] = "'" + param_dict['value'] + "'"
					where_part += '%s %s %s AND ' % (param_dict['field'], param_dict['comparator'], param_dict['value'])
				where_part = where_part[:-4]
		else:
			print('Need to have params for select. Called it with:', table, param_list, where_param_dicts, debug)
			return
		
		query = 'SELECT %s FROM %s' % (field_list, table)
		if where_part or where_literal:
			query = '%s WHERE' % (query)
			if where_part:
				query = '%s %s' % (query, where_part)
			if where_literal:
				if len(where_literal)>0:
					query = '%s %s' % (query, where_literal)
		self._prepare(query)
		self._attach_where_params(where_param_dicts)
		self._execute('SELECT', query, debug)
		return self._fetch(param_list)
	
	def table_list(self):
		if self.backend == 'SQLITE':
			self._execute('\dt', """SELECT name FROM sqlite_master
WHERE type='table'
ORDER BY name""", False)
		else:
			self._execute('\dt', """SELECT c.relname as "Name"
FROM pg_catalog.pg_class c
     LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind IN ('r','')
      AND n.nspname <> 'pg_catalog'
      AND n.nspname <> 'information_schema'
      AND n.nspname !~ '^pg_toast'
  AND pg_catalog.pg_table_is_visible(c.oid)""", False)
		
		fetched = self._fetch(('Name', ))
		
		result = []
		for item in fetched:
			result.append(item['Name'])
		
		return result
	
	def transaction_begin(self):
		self.database.transaction()
	
	def transaction_commit(self):
		if not self.database.commit():
			self.msg.message_warning("failed DB commit")
	
	#def update(self, table: str, param_dict: Dict[str,Any], where_param_dicts: List[Dict[str,Any]], debug=False) -> None: #TODO rename where_param_dict to where_param_tuples
	def update(self, table: str, param_dict, where_param_dicts=[], debug=False) -> None: #TODO rename where_param_dict to where_param_tuples
		set_part = ''
		if len(param_dict) > 0:
			for key in param_dict.keys():
				set_part += '%s = :%s, ' % (key, key)
			set_part = set_part[:-2]
		else:
			print('Need to have params for update. Called it with:', table, param_dict, where_param_dicts, debug)
			return
		
		where_part = ''
		if len(where_param_dicts) > 0:
				for where_param_dict in where_param_dicts: #TODO apply this to all other methods, or better, unify code
					if type(where_param_dict['value']) == str:
						where_param_dict['value'] = where_param_dict['value'].replace("'", "") #TODO remove once i attach params properly
						if self.backend == 'SQLITE':
							where_param_dict['value'] = '"' + where_param_dict['value'] + '"'
						else:
							where_param_dict['value'] = "'" + where_param_dict['value'] + "'"
					where_part += '%s %s %s AND ' % (where_param_dict['field'], where_param_dict['comparator'], where_param_dict['value'])
				where_part = where_part[:-4]
		else:
			print('Need to have where for update. Called it with:', table, param_dict, where_param_dicts, debug)
			return
		query = 'UPDATE %s SET %s WHERE %s' % (table, set_part, where_part)
		self._prepare(query)
		self._attach_params(param_dict)
		self._attach_where_params(where_param_dicts)
		self._execute('UPDATE', query, debug)
	
	def value(self, number: int):
		return self.cursor.value(number)
