#!/usr/bin/env python3.4
# -*- coding: utf8 -*-

# Copyright (C) 2015 Steffen Schaumburg and contributors, see docs/contributors.txt <steffen@schaumburger.info>
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
# In the original distribution you can find the license in docs/agpl_3.0.txt.


#python std lib
from argparse import ArgumentParser
import datetime
import os
import pickle
import random
import shutil
import signal
import sys

#PyQt modules
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTabWidget

#other 3rd party libs
#TODO import typing

#own modules
#TODO from RecreateTables import RecreateTables
#TODO from import_worlds import ImportWorlds
from catlib.messenger import Messenger
from catlib.SQL_feeder import SQLFeeder
from catlib.tab_DB_info import TabDBInfo
from report_parser import ReportParser
from game_data import GameData
from tab_filter import TabFilter
from tab_targets import TabTargets
from user_settings import SQLFEEDER_BACKEND

class Pytw(QMainWindow):
	def __init__(self):
		super(Pytw, self).__init__()
		#CLI args
		parser = ArgumentParser(description="pytw")
		parser.add_argument('--debug', help="activate debug mode", action='store_true')
		self.args = parser.parse_args()
		
		#messenger
		self.msg = Messenger(self.args, "pytw")
		self.msg.message_debug("Args: %s" % str(self.args))
		self.home_path = self.msg.home_path
		
		#setup the sqlite DB and data
		self.sql = SQLFeeder(self.msg, SQLFEEDER_BACKEND, 'pytw')
		self.game_data = GameData(self.sql)
		
		#setup window
		with open(os.path.join('src', 'version.ini'), 'r') as infile:
			self.version = infile.readlines()[0][:-1]
		self.msg.message_debug("Version %s" % self.version)
		self.setWindowTitle("Pytw %s" % self.version)
		self.resize(1200, 330) #TODO flexibilise
		
		#General tab init
		self.tab_widget = QTabWidget()
		self.tab_widget.currentChanged.connect(self.current_tab_changed)
		self.setCentralWidget(self.tab_widget)
		self.tabs = {}
		
		#check DB is valid
		try:
		#if True:
			self.sql.select(table='general', param_list=('value', ), where_param_dicts=({'field':'id', 'comparator':'=', 'value':'schema_version'}, ))
		except: #TODO specify error type
			print("DB seems invalid, please fix or recreate tables")
			self.quit()
		
		self.report_parser = ReportParser(self.msg, self.sql)
		
		self.add_tab(TabFilter(self.msg, self.game_data))
		self.add_tab(TabTargets(self.msg, self.sql, self.game_data, self.tabs['Filter'].filter))
		self.add_tab(TabDBInfo(self.sql))
		self.find_attacking_cities()
		
		self.setup_toolbar()
		self.show()
	
	def add_tab(self, new_tab):
		self.msg.message_debug("adding tab %s" % new_tab.name)
		self.tab_widget.addTab(new_tab.scroller, new_tab.name)
		self.tabs[new_tab.name] = new_tab
	
	def current_tab_changed(self, index):
		if index == 1: #Targets
			self.tabs['Targets'].draw()
	
	def find_attacking_cities(self):
		self.attacking_cities = []
		attackers = self.sql.select(table='battles', param_list=('DISTINCT attacker_village_id', ))
		for attacker in attackers:
			attacker_details = self.sql.select(table='villages', param_list=('id', 'village_name', 'location_x', 'location_y'), where_param_dicts = ({'field':'id', 'comparator':'=', 'value':attacker['DISTINCT attacker_village_id']}, ))
			self.attacking_cities.append(attacker_details[0])
		
		self.tabs["Filter"].replace_attacking_cities(self.attacking_cities)
		print('found attackers:', self.attacking_cities)
	
	def import_reports(self):
		overall_start = datetime.datetime.now()
		count = 0
		for filename in os.listdir(os.path.join('.', 'import', 'reports')):
			if filename == '.keep':
				continue
			file_start = datetime.datetime.now()
			count += 1
			file_path = os.path.join('.', 'import', 'reports', filename)
			target_path = os.path.join('.', 'import', 'reports-imported', datetime.datetime.strftime(file_start, '%Y-%m-%d_%H-%M-%S-%f__') + filename)
			with open(file_path, 'r') as infile:
				#print("importing", os.path.join('.', 'import', 'reports', filename))
				self.report_parser.parse(infile.read(), file_path, target_path)
			shutil.move(file_path, target_path) #TODO only iff target filename doesnt exist
			#print("   took", datetime.datetime.now()-file_start)
		print('imported', count, "files, took", datetime.datetime.now()-overall_start, 'seconds')
		if count > 0:
			self.current_tab_changed(self.tab_widget.currentIndex()) #to only redraw if active tab is targets
		self.find_attacking_cities()
	
	def quit(self): #TODO commit&close DBs
		print("start of Pytw.quit")
		self.msg.message_debug("Terminating Pytw normally")
		sys.exit(0)
	
	def refresh_views(self):
		for tab in self.tabs.values():
			tab.draw()
	
	def setup_toolbar(self):
		self.toolbar = self.addToolBar('')
		
		#TODO action = self.toolbar.addAction('Recreate Tables', self.recreate_tables)
		#self.addAction(action)
		
		#action = self.toolbar.addAction('Refresh Views', self.refresh_views)
		#action.setShortcut('F5')
		#self.addAction(action)
		
		#action = self.toolbar.addAction('Find Attacking Cities', self.find_attacking_cities)
		#action.setShortcut('Ctrl+F')
		#self.addAction(action)
		
		action = self.toolbar.addAction('Import Reports', self.import_reports)
		action.setShortcut('Ctrl+I')
		self.addAction(action)
		
		action = self.toolbar.addAction(QIcon.fromTheme('quit'), 'Quit', self.quit) #TODO: it doesnt display the icon
		action.setShortcut('Ctrl+Q')
		self.addAction(action)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	signal.signal(signal.SIGINT, signal.SIG_DFL) #makes ctrl+C at the shell work
	pytw = Pytw()
	
	sys.exit(app.exec_())
