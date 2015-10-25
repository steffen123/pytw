#!/usr/bin/env python3.4
# -*- coding: utf8 -*-

# Copyright (C) 2015 Steffen Schaumburg and contributors, see docs/contributors.txt <steffen@schaumburger.info>
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
# In the original distribution you can find the license in docs/agpl_3.0.txt.

#python std lib
import os
import re
import sys

#mypy
#import typing

#PyQt modules
#from PyQt5.QtCore import QObject, Qt
#from PyQt5.QtSql import QSqlRelationalTableModel
#from PyQt5.QtWidgets import QLabel, QPushButton, QTextEdit

#own modules
from catlib.messenger import Messenger
from catlib.SQLFeeder import SQLFeeder
from user_settings import SQLFEEDER_BACKEND

class ImportWorlds(object):
	def __init__(self, sql):
		self.sql = sql
		
		for filepath in os.listdir(os.path.join('.', 'import', 'world_settings')):
			domain = filepath.split('.')[0]
			print(domain)
			self.sql.insert(table='worlds', param_dict={'world_string':domain}, debug=False)
			world_id = self.sql.last_insert_id()
			
			self.sql.insert(table='players', param_dict={'inno_player_id':0, 'player_name':'Barbaren', 'world_id':world_id}, debug=False) #TODO: tribe abbreviation

if __name__ == '__main__':
	messenger = Messenger(args=None, name="pytw", has_GUI=False)
	sql = SQLFeeder(messenger, SQLFEEDER_BACKEND, 'pytw')
	muh = ImportWorlds(sql)
	sys.exit(0)
