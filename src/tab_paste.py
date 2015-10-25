# -*- coding: utf8 -*-

# Copyright (C) 2015 Steffen Schaumburg and contributors, see docs/contributors.txt <steffen@schaumburger.info>
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
# In the original distribution you can find the license in docs/agpl_3.0.txt.

#mypy
#import typing

#PyQt modules
#from PyQt5.QtCore import QObject, Qt
#from PyQt5.QtSql import QSqlRelationalTableModel
from PyQt5.QtWidgets import QLabel, QPushButton, QTextEdit

#own modules
from catlib.GridScrollTab import GridScrollTab

class TabPaste(GridScrollTab):
	def __init__(self, sql, parser):
		super(TabPaste, self).__init__()
		self.name = "Paste"
		self.sql = sql
		self.parser = parser 
		
		current_x = 1
		current_y = 1
		
		self.layout.addWidget(QLabel("Paste below"), current_y, current_x, 1, 1)
		current_y += 1
		
		self.paste_area = QTextEdit()
		self.layout.addWidget(self.paste_area, current_y, current_x, 1, 1)
		current_y += 1
		
		self.add_button = QPushButton("Add")
		self.layout.addWidget(self.add_button, current_y, current_x, 1, 1)
		current_y += 1
		self.add_button.clicked.connect(self.add_clicked)
	
	#def draw(self):
	#	self.model.select()
	
	def add_clicked(self, meh):
		self.parser.parse(self.paste_area.toPlainText())
