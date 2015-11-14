# -*- coding: utf8 -*-

# Copyright (C) 2015 Steffen Schaumburg and contributors, see docs/contributors.txt <steffen@schaumburger.info>
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
# In the original distribution you can find the license in docs/agpl_3.0.txt.

#python stdlib
import datetime
import math
import webbrowser

#mypy
#import typing

#PyQt modules
#from PyQt5.QtCore import QObject, Qt
#from PyQt5.QtSql import QSqlRelationalTableModel
from PyQt5.QtWidgets import QComboBox, QLabel, QLineEdit, QPushButton, QTextEdit

#own modules
from catlib.grid_scroll_tab import GridScrollTab
from constants import DEFAULT_FILTER

class TabFilter(GridScrollTab):
	def __init__(self, msg, game_data):
		super(TabFilter, self).__init__()
		self.name = "Filter"
		self.msg = msg
		self.game_data = game_data
		self.filter = DEFAULT_FILTER
		
		self.draw()
	
	def draw(self):
		while(True): #TODO move this into superclass
			item = self.layout.takeAt(0)
			if not item:
				break
			item.widget().deleteLater()
		
		self.comparator_combos = {}
		self.comparator_lines = {}
		current_x = 0
		current_y = 0
		
		
		self.layout.addWidget(QLabel("player and/or barbarian?"), current_y, current_x, 1, 1)
		current_x += 1
		
		self.combo_barbarian = QComboBox()
		count = 0
		for item in ("only players", "only barbarians", "both"):
			self.combo_barbarian.addItem(item)
			if item == self.filter['player or barb']:
				self.combo_barbarian.setCurrentIndex(count)
			count += 1
		self.combo_barbarian.currentIndexChanged.connect(self.filter_changed)
		self.layout.addWidget(self.combo_barbarian, current_y, current_x, 1, 1)
		current_x = 0
		current_y += 1
		
		
		for filter_name in ('wall', 'unit count', 'spied res', 'last loot', 'expected loot', 'distance'):
			self.layout.addWidget(QLabel(filter_name), current_y, current_x, 1, 1)
			current_x += 1
			
			self.comparator_combos[filter_name] = QComboBox()
			count = 0
			for comparator in ('>', '>=', '=', '<=', '<'):
				self.comparator_combos[filter_name].addItem(comparator)
				if comparator == self.filter[filter_name + ' comparator']:
					self.comparator_combos[filter_name].setCurrentIndex(count)
				count += 1
			self.comparator_combos[filter_name].currentIndexChanged.connect(self.filter_changed)
			self.layout.addWidget(self.comparator_combos[filter_name], current_y, current_x, 1, 1)
			current_x += 1
		
			self.comparator_lines[filter_name] = QLineEdit()
			self.comparator_lines[filter_name].insert(str(self.filter[filter_name]))
			self.comparator_lines[filter_name].editingFinished.connect(self.filter_changed)
			self.layout.addWidget(self.comparator_lines[filter_name], current_y, current_x, 1, 1)
			current_x = 0
			current_y += 1
		
		self.layout.addWidget(QLabel("slowest unit"), current_y, current_x, 1, 1)
		current_x += 1
		
		self.combo_speed = QComboBox()
		count = 0
		for unit_name in sorted(self.game_data.units.keys()):
			self.combo_speed.addItem(unit_name)
			if unit_name == self.filter['slowest unit']:
				self.combo_speed.setCurrentIndex(count)
			count += 1
		self.combo_speed.currentIndexChanged.connect(self.filter_changed)
		self.layout.addWidget(self.combo_speed, current_y, current_x, 1, 1)
		current_x = 0
		current_y += 1
	
	def filter_changed(self, something=None):
		if self.combo_barbarian.currentIndex() == 0:
			self.filter['player or barb'] = 'only players'
		elif self.combo_barbarian.currentIndex() == 1:
			self.filter['player or barb'] = 'only barbarians'
		else:
			self.filter['player or barb'] = 'both'
		
		for name, comparator_combo in self.comparator_combos.items():
			if comparator_combo.currentIndex() == 0:
				self.filter[name + ' comparator'] = '>'
			elif comparator_combo.currentIndex() == 1:
				self.filter[name + ' comparator'] = '>='
			elif comparator_combo.currentIndex() == 2:
				self.filter[name + ' comparator'] = '='
			elif comparator_combo.currentIndex() == 3:
				self.filter[name + ' comparator'] = '<='
			elif comparator_combo.currentIndex() == 4:
				self.filter[name + ' comparator'] = '<'
			
			if name == 'distance':
				self.filter[name] = float(self.comparator_lines[name].text())
			else:
				self.filter[name] = int(self.comparator_lines[name].text())
		
		self.filter['slowest unit'] = sorted(self.game_data.units.keys())[self.combo_speed.currentIndex()]
