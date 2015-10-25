# -*- coding: utf8 -*-

# Copyright (C) 2014-2015 Steffen Schaumburg and contributors, see docs/contributors.txt <steffen@schaumburger.info>
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
# In the original distribution you can find the license in docs/agpl_3.0.txt.

#TODO unify no-logger handling into a method

#python std lib
from datetime import datetime
import logging
import os
import sys

#other 3rd party libs
#from typing import Any

#PyQt modules
from PyQt5.QtWidgets import QMessageBox

class Messenger():
	#def __init__(self, args: Any, name: str, has_GUI = True) -> None: #TODO don't use Any here
	def __init__(self, args, name: str, has_GUI = True) -> None:
		self.args = args
		self.has_GUI = has_GUI
		
		self.home_path = os.path.join(os.path.expanduser("~"), '.%s' % name)
		if not os.path.exists(self.home_path):
			os.mkdir(self.home_path)
		
		self.logger = logging.getLogger(name)
		self.logger.setLevel(logging.DEBUG)
		file_logger = logging.FileHandler(os.path.join(self.home_path, '%s.log' % name))
		file_logger.setLevel(logging.DEBUG)
		self.logger.addHandler(file_logger)
		
		#TODO remove below?
		#if not self.args.dont_redirect_output:
		#	now = datetime.now()
		#	#self.stdout = sys.stdout
		#	#self.stderr = sys.stderr
		#	sys.stdout = open(os.path.join(self.home_path, '%s.stdout-%s.log' % (name, now)), 'w')
		#	sys.stderr = open(os.path.join(self.home_path, '%s.stderr-%s.log' % (name, now)), 'w')
	
	def message_debug(self, message: str) -> None: #TODO unify  methods into a flexible internal base method
		if self.logger:
			self.logger.debug(str(datetime.now()) + " " + message)
			try:
				if self.args.debug:
					print("%s DEBUG: %s" % (str(datetime.now()), message))
			except AttributeError: #when launched from lesser classes like CreatePak*
				print("%s DEBUG: %s" % (str(datetime.now()), message))
		else:
			if self.has_GUI:
				QMessageBox.critical(self, "Debug", "Logging inactive\n%s" % message)
	
	def message_fatal(self, message: str) -> None:
		message = "Fatal Error\nMessage: " + str(datetime.now()) + ".\n" + message
		if self.logger:
			self.logger.critical(message)
		else:
			print("Logger not initialised yet, cannot log the message")
		
		try:
			if self.args.debug:
				print(message)
		except AttributeError: #when launched from lesser classes like CreatePak*
			print(message)
		
		if self.has_GUI:
			QMessageBox.critical(self, "Fatal Error", message) #TODO this doesnt work anymore
		sys.exit(1)
	
	def message_warning(self, message: str) -> None:
		if self.logger:
			self.logger.warning(str(datetime.now()) + " " + message)
			try:
				if self.args.debug:
					print("WARNING: %s" % str(datetime.now()), message)
			except AttributeError: #when launched from lesser classes like CreatePak*
				print("WARNING: %s" % str(datetime.now()), message)
			if self.has_GUI:
				QMessageBox.warning(self, "Warning", message)
		else:
			if self.has_GUI:
				QMessageBox.critical(self, "Warning", "Logging inactive\n"+message)

