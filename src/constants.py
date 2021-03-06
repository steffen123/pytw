# -*- coding: utf8 -*-

# Copyright (C) 2014-2015 Steffen Schaumburg and contributors, see docs/contributors.txt <steffen@schaumburger.info>
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
# In the original distribution you can find the license in docs/agpl_3.0.txt.

#other 3rd party libs
#import typing

DB_VERSION = 4
DEFAULT_FILTER = {'player or barb':'both',
				  'wall comparator':'<=', 'wall':1,
				  'unit count comparator':'<=', 'unit count':1,
				  'spied res comparator':'>=', 'spied res':0,
				  'last loot comparator':'>=', 'last loot':0,
				  'expected loot comparator':'>=', 'expected loot':0,
				  'distance comparator':'>=', 'distance':0.0,
				  'slowest unit':'lcav',
				  'attacking_village_id':1}
