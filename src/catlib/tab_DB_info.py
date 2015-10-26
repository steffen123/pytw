# -*- coding: utf8 -*-

# Copyright (C) 2014-2015 Steffen Schaumburg and contributors, see docs/contributors.txt <steffen@schaumburger.info>
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
# In the original distribution you can find the license in docs/agpl_3.0.txt.

#PyQt modules
from PyQt5.QtWidgets import QLabel

#other 3rd party libs
#import typing

#own modules
from .grid_scroll_tab import GridScrollTab

class TabDBInfo(GridScrollTab):
	def __init__(self, sql, name="DB Info"):
		super(TabDBInfo, self).__init__()
		self.name = name
		self.sql = sql
		
		self.draw()
	
	def draw(self):
		while(True): #TODO move this into superclass
			item = self.layout.takeAt(0)
			if not item:
				break
			item.widget().deleteLater()
		
		row_counter = 0
		column_counter = 0
		for table_name in self.sql.table_list():
			row_count = len(self.sql.select(table_name, ("id", ), {}))
			self.layout.addWidget(QLabel("Rows in %s: %d" % (table_name, row_count)), row_counter, column_counter, 1, 1)
			row_counter += 1
