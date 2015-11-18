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

class TabTargets(GridScrollTab):
	def __init__(self, msg, sql, game_data, filter):
		super(TabTargets, self).__init__()
		self.name = "Targets"
		self.msg = msg
		self.sql = sql
		self.game_data = game_data
		self.filter = filter
		
		self.headers = ("report", "village_name", "report date", "coordinates", "wall", "unit_count", "spied_res", "last_loot", "distance", "attack", "delete")
		
		self.draw()
	
	def draw(self):
		while(True): #TODO move this into superclass
			item = self.layout.takeAt(0)
			if not item:
				break
			item.widget().deleteLater()
		
		current_x = 0
		current_y = 0
		
		
		if self.filter['player or barb'] == 'only players':
			where_literal = 'village_name != "Barbarendorf" AND village_name != "Bonusdorf" AND '
		elif self.filter['player or barb'] == 'only barbarians':
			where_literal = '(village_name = "Barbarendorf" OR village_name = "Bonusdorf") AND '
		else:
			where_literal = ''
		
		
		where_literal += 'wall %s %s ' % (self.filter['wall comparator'], self.filter['wall'])
		
		where_literal += 'AND (defender_spears_sent + defender_swords_sent + defender_axes_sent + defender_archers_sent + defender_scouts_sent + defender_lcav_sent + defender_mounted_archers_sent + defender_hcav_sent + defender_rams_sent + defender_catapults_sent + defender_paladin_sent + defender_noblemen_sent + defender_militia_sent) %s %s ' % (self.filter['unit count comparator'], self.filter['unit count'])
		
		where_literal += 'AND (spied_wood + spied_clay + spied_iron) %s %s ' % (self.filter['spied res comparator'], self.filter['spied res'])
		
		where_literal += 'AND (looted_wood + looted_clay + looted_iron) %s %s ' % (self.filter['last loot comparator'], self.filter['last loot'])
		
		for header in self.headers:
			self.layout.addWidget(QLabel(header), current_y, current_x, 1, 1)
			current_x += 1
		current_y += 1
		current_x = 0
		
		
		targets = self.sql.select(table="battles INNER JOIN villages ON battles.defender_village_id = villages.id", param_list=('location_x', 'location_y', 'village_name', 'battle_ts', 'spied_wood', 'spied_clay', 'spied_iron', 'timber_camp', 'clay_pit', 'iron_mine', 'attacker_village_id', 'defender_village_id', 'battles.id', 'file_path_after_move', 'wall', 'defender_spears_sent', 'defender_swords_sent', 'defender_axes_sent', 'defender_archers_sent', 'defender_scouts_sent', 'defender_lcav_sent', 'defender_mounted_archers_sent', 'defender_hcav_sent', 'defender_rams_sent', 'defender_catapults_sent', 'defender_paladin_sent', 'defender_noblemen_sent', 'defender_militia_sent', 'attacker_spears_sent', 'attacker_swords_sent', 'attacker_axes_sent', 'attacker_archers_sent', 'attacker_scouts_sent', 'attacker_lcav_sent', 'attacker_mounted_archers_sent', 'attacker_hcav_sent', 'attacker_rams_sent', 'attacker_catapults_sent', 'attacker_paladin_sent', 'attacker_noblemen_sent', 'attacker_spears_lost', 'attacker_swords_lost', 'attacker_axes_lost', 'attacker_archers_lost', 'attacker_scouts_lost', 'attacker_lcav_lost', 'attacker_mounted_archers_lost', 'attacker_hcav_lost', 'attacker_rams_lost', 'attacker_catapults_lost', 'attacker_paladin_lost', 'attacker_noblemen_lost', 'looted_wood', 'looted_clay', 'looted_iron', 'hiding_place', 'warehouse'), where_param_dicts=None, where_literal=where_literal, debug=False)
		
		for target in targets:
			is_current_attack_target = self.sql.select(table="scheduled_attacks", param_list=('defender_village_id', ), where_param_dicts=({'field':'defender_village_id', 'comparator':'=', 'value':target['defender_village_id']}, {'field':'arrival_ts', 'comparator':'>', 'value':"'"+str(datetime.datetime.now())+"'"}), debug=False)
			if is_current_attack_target:
				continue
			
			delta_hours = (datetime.datetime.now() - datetime.datetime.strptime(target['battle_ts'], '%Y-%m-%d %H:%M:%S.%f')).seconds/3600
			target["distance"] = self.game_data.distance(target['attacker_village_id'], target['defender_village_id'])
			if not self.multi_compare(target["distance"], self.filter['distance comparator'], float(self.filter['distance'])):
				continue
			
			if target['spied_wood'] == '':
				target['spied_wood'] = 0
			if target['spied_clay'] == '':
				target['spied_clay'] = 0
			if target['spied_iron'] == '':
				target['spied_iron'] = 0
			
			if type(target['spied_wood']) == str:
				target['spied_wood'] = int(target['spied_wood'])
			if type(target['spied_clay']) == str:
				target['spied_clay'] = int(target['spied_clay'])
			if type(target['spied_iron']) == str:
				target['spied_iron'] = int(target['spied_clay'])
			
			target['spied_res'] = target['spied_wood'] + target['spied_clay'] + target['spied_iron']
			
			oneway_time = self.game_data.oneway_time(target["distance"], self.filter['slowest unit'])
			
			wood = target['spied_wood'] + round(48 * math.pow(1.163118, target['timber_camp']-1) / 1.6 * (delta_hours + oneway_time))
			clay = target['spied_clay'] + round(48 * math.pow(1.163118, target['clay_pit']-1) / 1.6 * (delta_hours + oneway_time))
			iron = target['spied_iron'] + round(48 * math.pow(1.163118, target['iron_mine']-1) / 1.6 * (delta_hours + oneway_time))
			
			max_storage = self.game_data.max_storage(target['warehouse'], target['hiding_place'])
			if wood > max_storage:
				wood = max_storage
			if clay > max_storage:
				clay = max_storage
			if iron > max_storage:
				iron = max_storage
			expected_loot = wood + clay + iron
			
			if not self.multi_compare(expected_loot, self.filter['expected loot comparator'], int(self.filter['expected loot'])):
				continue
			
			
			total_loot_capacity = 0
			for unit_name, unit_dict in self.game_data.units.items():
				if unit_name == 'militia':
					continue
				
				total_loot_capacity += (target['attacker_%s_sent' % unit_name] - target['attacker_%s_lost' % unit_name]) * unit_dict['loot_capacity']
			total_looted = target['looted_wood'] + target['looted_clay'] + target['looted_iron']
			
			target['unit_count'] = target['defender_spears_sent'] + target['defender_swords_sent'] + target['defender_axes_sent'] + target['defender_archers_sent'] + target['defender_scouts_sent'] + target['defender_lcav_sent'] + target['defender_mounted_archers_sent'] + target['defender_hcav_sent'] + target['defender_rams_sent'] + target['defender_catapults_sent'] + target['defender_paladin_sent'] + target['defender_noblemen_sent'] + target['defender_militia_sent']
			
			for field in self.headers:
				if field == "attack":
					if self.game_data.units[self.filter['slowest unit']]['loot_capacity'] > 0:
						button = QPushButton("%dres, %.1f%s" % (expected_loot, expected_loot/self.game_data.units[self.filter['slowest unit']]['loot_capacity'], self.filter['slowest unit']))
					else:
						button = QPushButton("%dres, %s" % (expected_loot, self.filter['slowest unit']))
					button.setProperty('attacker_village_id', target['attacker_village_id'])
					button.setProperty('defender_village_id', target['defender_village_id'])
					button.setProperty('attacking_unit', self.filter['slowest unit'])
					button.setProperty('oneway_time', oneway_time)
					button.clicked.connect(self.attack_button_clicked)
					self.layout.addWidget(button, current_y, current_x, 1, 1)
				elif field == "delete":
					button = QPushButton(field)
					button.setProperty('battle_id', target['battles.id'])
					button.setProperty('defender_village_id', target['defender_village_id'])
					button.clicked.connect(self.delete_button_clicked)
					self.layout.addWidget(button, current_y, current_x, 1, 1)
				elif field == "report":
					button = QPushButton("view")
					button.setProperty('file_path', target['file_path_after_move'])
					button.clicked.connect(self.report_button_clicked)
					self.layout.addWidget(button, current_y, current_x, 1, 1)
				elif field == "distance":
					self.layout.addWidget(QLabel('%.1f' % target[field]), current_y, current_x, 1, 1)
				elif field == "report date":
					self.layout.addWidget(QLabel(datetime.datetime.strptime(target['battle_ts'], '%Y-%m-%d %H:%M:%S.%f').strftime('%d%b %H:%M')), current_y, current_x, 1, 1) #TODO remove crazy conversion once DB returns it properly +'000'
				elif field == "last_loot":
					self.layout.addWidget(QLabel('%s/%s' % (total_looted, total_loot_capacity)), current_y, current_x, 1, 1)
				elif field == "coordinates":
					edit = QLineEdit()
					edit.insert('%d|%d' % (target['location_x'], target['location_y']))
					self.layout.addWidget(edit, current_y, current_x, 1, 1)
				else:
					self.layout.addWidget(QLabel(str(target[field])), current_y, current_x, 1, 1)
				
				current_x += 1
			current_y += 1
			current_x = 0
	
	def attack_button_clicked(self, TODO_dunno):
		attacker_village_id = self.sender().property('attacker_village_id')
		defender_village_id = self.sender().property('defender_village_id')
		attacking_unit = self.sender().property('attacking_unit')
		oneway_time = self.sender().property('oneway_time')
		
		self.sql.insert(table='scheduled_attacks', param_dict={'attacker_village_id':attacker_village_id, 'defender_village_id':defender_village_id, 'is_attack':True, 'slowest_unit':attacking_unit, 'launch_ts':datetime.datetime.now(), 'arrival_ts':datetime.datetime.now() + datetime.timedelta(hours=oneway_time), 'return_ts':datetime.datetime.now() + datetime.timedelta(hours=2*oneway_time)}, debug=False)
		self.draw()
	
	def delete_button_clicked(self, TODO_dunno):
		battle_id = self.sender().property('battle_id')
		self.sql._execute("JUST RUN IT", 'DELETE FROM battles WHERE id = %d' % battle_id, False)
		
		defender_village_id = self.sender().property('defender_village_id')
		self.sql._execute("JUST RUN IT", 'DELETE FROM villages WHERE id = %d' % defender_village_id, False)
		
		self.draw()
	
	def multi_compare(self, value_1, comparator, value_2):
		if comparator == '>':
			if value_1 > value_2:
				return True
		elif comparator == '>=':
			if value_1 >= value_2:
				return True
		elif comparator == '=':
			if value_1 == value_2:
				return True
		elif comparator == '<=':
			if value_1 <= value_2:
				return True
		elif comparator == '<':
			if value_1 < value_2:
				return True
		
		return False
	
	def report_button_clicked(self, TODO_dunno):
		file_path = self.sender().property('file_path')
		webbrowser.open(file_path)
