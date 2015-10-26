# -*- coding: utf8 -*-

# Copyright (C) 2014-2015 Steffen Schaumburg and contributors, see docs/contributors.txt <steffen@schaumburger.info>
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
# In the original distribution you can find the license in docs/agpl_3.0.txt.

#PyQt modules
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QGridLayout, QLayout, QScrollArea, QWidget

#other 3rd party libs
#import typing

#own modules

class GridScrollTab(QObject):
	def __init__(self) -> None:
		super(GridScrollTab, self).__init__()
		
		self.model = None
		
		self.scroller = QScrollArea()
		self.widget = QWidget()
		self.layout = QGridLayout()
		self.layout.setSizeConstraint(QLayout.SetMinAndMaxSize)
		self.widget.setLayout(self.layout)
		self.scroller.setWidget(self.widget)
