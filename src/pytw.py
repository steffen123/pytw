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
from report_parser import ReportParser
from tab_targets import TabTargets
from catlib.messenger import Messenger
from catlib.SQLFeeder import SQLFeeder
from catlib.TabDBInfo import TabDBInfo
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
		
		#setup the sqlite DB
		self.sql = SQLFeeder(self.msg, SQLFEEDER_BACKEND, 'pytw')
		
		#setup window
		with open(os.path.join('src', 'version.ini'), 'r') as infile:
			self.version = infile.readlines()[0][:-1]
		self.msg.message_debug("Version %s" % self.version)
		self.setWindowTitle("Pytw %s" % self.version)
		self.resize(1500, 800) #TODO flexibilise
		
		#General tab init
		self.tab_widget = QTabWidget()
		self.setCentralWidget(self.tab_widget)
		self.tabs = {}
		
		#check DB is valid
		try:
		#if True:
			self.sql.select(table='general', param_list=('value', ), where_param_dicts=({'field':'id', 'comparator':'=', 'value':'schema_version'}, ))
		except: #TODO specify error type
			print("DB seems invalid, please fix or recreate tables")
			self.quit()
		
		self.report_parser = ReportParser(self.sql)
		
		self.add_tab(TabTargets(self.msg, self.sql))
		self.add_tab(TabDBInfo(self.sql))
		
		self.setup_toolbar()
		self.show()
	
	def add_tab(self, new_tab):
		self.msg.message_debug("adding tab %s" % new_tab.name)
		self.tab_widget.addTab(new_tab.scroller, new_tab.name)
		self.tabs[new_tab.name] = new_tab
	
	def import_reports(self):
		overall_start = datetime.datetime.now()
		count = 0
		for filename in os.listdir(os.path.join('.', 'reports')):
			file_start = datetime.datetime.now()
			count += 1
			with open(os.path.join('.', 'reports', filename), 'r') as infile:
				print("importing", os.path.join('.', 'reports', filename))
				self.report_parser.parse(infile.read())
			print("   took", datetime.datetime.now()-file_start)
		print('\n', count, "files, took", datetime.datetime.now()-overall_start)
		if count > 0:
			self.refresh_views()
	
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
		
		action = self.toolbar.addAction('Refresh Views', self.refresh_views)
		action.setShortcut('F5')
		self.addAction(action)
		
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
