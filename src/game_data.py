# -*- coding: utf8 -*-

# Copyright (C) 2015 Steffen Schaumburg and contributors, see docs/contributors.txt <steffen@schaumburger.info>
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
# In the original distribution you can find the license in docs/agpl_3.0.txt.

#mypy
import math
#import typing

#own modules

class GameData():
	def __init__(self, sql):
		self.sql = sql
		
		self.units = {'spears':{'loot_capacity':25}, 'swords':{'loot_capacity':15}, 'axes':{'loot_capacity':10}, 'archers':{'loot_capacity':10}, 'scouts':{'loot_capacity':0}, 'lcav':{'loot_capacity':80}, 'mounted_archers':{'loot_capacity':50}, 'hcav':{'loot_capacity':50}, 'rams':{'loot_capacity':0}, 'catapults':{'loot_capacity':0}, 'paladin':{'loot_capacity':100}, 'noblemen':{'loot_capacity':0}, 'militia':{'loot_capacity':0}}
		self.unit_speeds = {'ram':30, 'sword':22, 'spear':18, 'lcav':10, 'scout':9} #TODO migrate to above
	
	def distance(self, attacker_village_id, defender_village_id):
		attacker = self.sql.select(table="villages", param_list=('location_x', 'location_y'), where_param_dicts=({'field':'id', 'comparator':'=', 'value':attacker_village_id}, ), debug=False)
		att_x = attacker[0]['location_x']
		att_y = attacker[0]['location_y']
		
		defender = self.sql.select(table="villages", param_list=('location_x', 'location_y'), where_param_dicts=({'field':'id', 'comparator':'=', 'value':defender_village_id}, ), debug=False)
		def_x = defender[0]['location_x']
		def_y = defender[0]['location_y']
		
		return math.sqrt(math.pow(att_x - def_x, 2) + math.pow(att_y - def_y, 2))
	
	def max_storage(self, warehouse, hiding_place):
		storage = 1000 * math.pow(1.2294934, warehouse - 1)
		hiding_place = 150 * math.pow(1.3335, hiding_place - 1)
		return storage - hiding_place
	
	def oneway_time(self, distance, attacking_unit):
		return distance * self.unit_speeds[attacking_unit] / 60
