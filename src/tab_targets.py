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
	def __init__(self, msg, sql):
		super(TabTargets, self).__init__()
		self.name = "Targets"
		self.msg = msg
		self.sql = sql
		
		self.headers = ("report", "village_name", "report date", "location", "wall", "unit_count", "spied_res", "last_loot", "distance", "attack", "delete")
		self.unit_speeds = {'ram':30, 'sword':22, 'spear':18, 'lcav':10, 'scout':9} #TODO migrate to below
		self.units = {'spears':{'loot_capacity':25}, 'swords':{'loot_capacity':15}, 'axes':{'loot_capacity':10}, 'archers':{'loot_capacity':10}, 'scouts':{'loot_capacity':0}, 'lcav':{'loot_capacity':80}, 'mounted_archers':{'loot_capacity':50}, 'hcav':{'loot_capacity':50}, 'rams':{'loot_capacity':0}, 'catapults':{'loot_capacity':0}, 'paladin':{'loot_capacity':100}, 'noblemen':{'loot_capacity':0}, 'militia':{'loot_capacity':0}}
		
		self.combo_barbarian = None
		self.combo_wall = None
		self.line_wall = None
		self.combo_units = None
		self.line_units = None
		self.combo_speed = None
		self.line_loot = None
		self.line_distance = None
		
		self.draw()
	
	def draw(self):
		if self.combo_barbarian:
			combo_barbarian_old_setting = self.combo_barbarian.currentIndex()
		else:
			combo_barbarian_old_setting = 0
		
		
		if self.combo_wall:
			combo_wall_old_setting = self.combo_wall.currentIndex()
		else:
			combo_wall_old_setting = 0
		
		if self.line_wall:
			line_wall_old_setting = self.line_wall.text()
		else:
			line_wall_old_setting = "0"
		
		
		if self.combo_units:
			combo_units_old_setting = self.combo_units.currentIndex()
		else:
			combo_units_old_setting = 0
		
		if self.line_units:
			line_units_old_setting = self.line_units.text()
		else:
			line_units_old_setting = "0"
		
		
		if self.combo_speed:
			combo_speed_old_setting = self.combo_speed.currentIndex()
		else:
			combo_speed_old_setting = 0
		
		if self.line_loot:
			line_loot_old_setting = self.line_loot.text()
		else:
			line_loot_old_setting = "600"
		
		
		if self.line_distance:
			line_distance_old_setting = self.line_distance.text()
		else:
			line_distance_old_setting = "50.0"
		
		
		while(True): #TODO move this into superclass
			item = self.layout.takeAt(0)
			if not item:
				break
			item.widget().deleteLater()
		
		
		current_x = 0
		current_y = 0
		
		
		self.combo_barbarian = QComboBox()
		for item in ("only Players", "only Barbarian", "Player+Barb"):
			self.combo_barbarian.addItem(item)
		self.combo_barbarian.setCurrentIndex(combo_barbarian_old_setting)
		self.combo_barbarian.currentIndexChanged.connect(self.draw)
		self.layout.addWidget(self.combo_barbarian, current_y, current_x, 1, 1)
		current_x += 1
		
		
		self.combo_wall = QComboBox()
		for item in ("max. wall", "min. wall", "= wall"):
			self.combo_wall.addItem(item)
		self.combo_wall.setCurrentIndex(combo_wall_old_setting)
		self.combo_wall.currentIndexChanged.connect(self.draw)
		self.layout.addWidget(self.combo_wall, current_y, current_x, 1, 1)
		current_x += 1
		
		self.line_wall = QLineEdit()
		self.line_wall.insert(line_wall_old_setting)
		self.line_wall.editingFinished.connect(self.draw)
		self.layout.addWidget(self.line_wall, current_y, current_x, 1, 1)
		current_x += 1
		
		
		self.combo_units = QComboBox()
		for item in ("max. units", "min. units", "= units"):
			self.combo_units.addItem(item)
		self.combo_units.setCurrentIndex(combo_units_old_setting)
		self.combo_units.currentIndexChanged.connect(self.draw)
		self.layout.addWidget(self.combo_units, current_y, current_x, 1, 1)
		current_x += 1
		
		self.line_units = QLineEdit()
		self.line_units.insert(line_units_old_setting)
		self.line_units.editingFinished.connect(self.draw)
		self.layout.addWidget(self.line_units, current_y, current_x, 1, 1)
		current_x += 1
		
		
		self.combo_speed = QComboBox()
		self.combo_speed_strings = []
		for unit_name in self.unit_speeds.keys():
			self.combo_speed.addItem("min. loot with %s" % unit_name)
			self.combo_speed_strings.append(unit_name)
		self.combo_speed.setCurrentIndex(combo_speed_old_setting)
		self.combo_speed.currentIndexChanged.connect(self.draw)
		self.layout.addWidget(self.combo_speed, current_y, current_x, 1, 1)
		current_x += 1
		
		self.line_loot = QLineEdit()
		self.line_loot.insert(line_loot_old_setting)
		self.line_loot.editingFinished.connect(self.draw)
		self.layout.addWidget(self.line_loot, current_y, current_x, 1, 1)
		current_x += 1
		
		self.layout.addWidget(QLabel("max. distance"), current_y, current_x, 1, 1)
		current_x += 1
		
		self.line_distance = QLineEdit()
		self.line_distance.insert(line_distance_old_setting)
		self.line_distance.editingFinished.connect(self.draw)
		self.layout.addWidget(self.line_distance, current_y, current_x, 1, 1)
		max_distance = float(line_distance_old_setting.replace(',','.'))
		current_x = 0
		current_y += 1
		
		
		for header in self.headers:
			self.layout.addWidget(QLabel(header), current_y, current_x, 1, 1)
			current_x += 1
		current_y += 1
		current_x = 0
		
		
		if self.combo_barbarian.currentIndex() == 0:
			where_literal = 'village_name != "Barbarendorf" AND village_name != "Bonusdorf" AND '
		elif self.combo_barbarian.currentIndex() == 1:
			where_literal = '(village_name = "Barbarendorf" OR village_name = "Bonusdorf") AND '
		else:
			where_literal = ''
		
		if self.combo_wall.currentIndex() == 0:
			where_literal += 'wall <= '
		elif self.combo_wall.currentIndex() == 1:
			where_literal += 'wall >= '
		else:
			where_literal += 'wall = '
		
		where_literal += self.line_wall.text() #TODO input error handling
		
		where_literal += ' AND (defender_spears_sent + defender_swords_sent + defender_axes_sent + defender_archers_sent + defender_scouts_sent + defender_lcav_sent + defender_mounted_archers_sent + defender_hcav_sent + defender_rams_sent + defender_catapults_sent + defender_paladin_sent + defender_noblemen_sent + defender_militia_sent) '
		
		if self.combo_units.currentIndex() == 0:
			where_literal += '<= '
		elif self.combo_units.currentIndex() == 1:
			where_literal += '>= '
		else:
			where_literal += '= '
		
		where_literal += self.line_units.text() #TODO input error handling
		
		
		targets = self.sql.select(table="battles INNER JOIN villages ON battles.defender_village_id = villages.id", param_list=('location_x', 'location_y', 'village_name', 'battle_ts', 'spied_wood', 'spied_clay', 'spied_iron', 'timber_camp', 'clay_pit', 'iron_mine', 'attacker_village_id', 'defender_village_id', 'battles.id', 'file_path', 'wall', 'defender_spears_sent', 'defender_swords_sent', 'defender_axes_sent', 'defender_archers_sent', 'defender_scouts_sent', 'defender_lcav_sent', 'defender_mounted_archers_sent', 'defender_hcav_sent', 'defender_rams_sent', 'defender_catapults_sent', 'defender_paladin_sent', 'defender_noblemen_sent', 'defender_militia_sent', 'attacker_spears_sent', 'attacker_swords_sent', 'attacker_axes_sent', 'attacker_archers_sent', 'attacker_scouts_sent', 'attacker_lcav_sent', 'attacker_mounted_archers_sent', 'attacker_hcav_sent', 'attacker_rams_sent', 'attacker_catapults_sent', 'attacker_paladin_sent', 'attacker_noblemen_sent', 'attacker_spears_lost', 'attacker_swords_lost', 'attacker_axes_lost', 'attacker_archers_lost', 'attacker_scouts_lost', 'attacker_lcav_lost', 'attacker_mounted_archers_lost', 'attacker_hcav_lost', 'attacker_rams_lost', 'attacker_catapults_lost', 'attacker_paladin_lost', 'attacker_noblemen_lost', 'looted_wood', 'looted_clay', 'looted_iron'), where_param_dicts=None, where_literal=where_literal, debug=False)
		
		for target in targets:
			is_current_attack_target = self.sql.select(table="scheduled_attacks", param_list=('defender_village_id', ), where_param_dicts=({'field':'defender_village_id', 'comparator':'=', 'value':target['defender_village_id']}, {'field':'arrival_ts', 'comparator':'>', 'value':"'"+str(datetime.datetime.now())+"'"}), debug=False)
			if is_current_attack_target:
				continue
			
			delta_hours = (datetime.datetime.now() - datetime.datetime.strptime(target['battle_ts'], '%Y-%m-%d %H:%M:%S.%f')).seconds/3600
			target["distance"] = self.calculate_distance(target['attacker_village_id'], target['defender_village_id'])
			if target["distance"] > max_distance:
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
			
			attacking_unit = self.combo_speed_strings[self.combo_speed.currentIndex()]
			oneway_time = self.calculate_oneway_time(target["distance"], attacking_unit)
			wood = target['spied_wood'] + round(48 * math.pow(1.163118, target['timber_camp']-1) / 1.6 * (delta_hours + oneway_time))
			clay = target['spied_clay'] + round(48 * math.pow(1.163118, target['clay_pit']-1) / 1.6 * (delta_hours + oneway_time))
			iron = target['spied_iron'] + round(48 * math.pow(1.163118, target['iron_mine']-1) / 1.6 * (delta_hours + oneway_time))
			expected_loot = wood + clay + iron
			if expected_loot < int(self.line_loot.text()):
				continue
			
			
			total_loot_capacity = 0
			for unit_name, unit_dict in self.units.items():
				if unit_name == 'militia':
					continue
				
				total_loot_capacity += (target['attacker_%s_sent' % unit_name] - target['attacker_%s_lost' % unit_name]) * unit_dict['loot_capacity']
			total_looted = target['looted_wood'] + target['looted_clay'] + target['looted_iron']
			
			target['unit_count'] = target['defender_spears_sent'] + target['defender_swords_sent'] + target['defender_axes_sent'] + target['defender_archers_sent'] + target['defender_scouts_sent'] + target['defender_lcav_sent'] + target['defender_mounted_archers_sent'] + target['defender_hcav_sent'] + target['defender_rams_sent'] + target['defender_catapults_sent'] + target['defender_paladin_sent'] + target['defender_noblemen_sent'] + target['defender_militia_sent']
			
			for field in self.headers:
				if field == "attack":
					button = QPushButton('loot %d' % expected_loot)
					button.setProperty('attacker_village_id', target['attacker_village_id'])
					button.setProperty('defender_village_id', target['defender_village_id'])
					button.setProperty('attacking_unit', attacking_unit)
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
					button.setProperty('file_path', target['file_path'])
					button.clicked.connect(self.report_button_clicked)
					self.layout.addWidget(button, current_y, current_x, 1, 1)
				elif field == "distance":
					self.layout.addWidget(QLabel('%.1f' % target[field]), current_y, current_x, 1, 1)
				elif field == "report date":
					self.layout.addWidget(QLabel(datetime.datetime.strptime(target['battle_ts'], '%Y-%m-%d %H:%M:%S.%f').strftime('%d%b %H:%M')), current_y, current_x, 1, 1) #TODO remove crazy conversion once DB returns it properly +'000'
				elif field == "last_loot":
					self.layout.addWidget(QLabel('%s/%s' % (total_looted, total_loot_capacity)), current_y, current_x, 1, 1)
				elif field == "location":
					self.layout.addWidget(QLabel('%d|%d' % (target['location_x'], target['location_y'])), current_y, current_x, 1, 1)
				else:
					self.layout.addWidget(QLabel(str(target[field])), current_y, current_x, 1, 1)
				
				current_x += 1
			current_y += 1
			current_x = 0
	
	def add_clicked(self, meh): #TODO reorder methods
		self.parser.parse(self.paste_area.toPlainText())
	
	def attack_button_clicked(self, TODO_dunno):
		attacker_village_id = self.sender().property('attacker_village_id')
		defender_village_id = self.sender().property('defender_village_id')
		attacking_unit = self.sender().property('attacking_unit')
		oneway_time = self.sender().property('oneway_time')
		
		self.sql.insert(table='scheduled_attacks', param_dict={'attacker_village_id':attacker_village_id, 'defender_village_id':defender_village_id, 'is_attack':True, 'slowest_unit':attacking_unit, 'launch_ts':datetime.datetime.now(), 'arrival_ts':datetime.datetime.now() + datetime.timedelta(hours=oneway_time)}, debug=False)
		self.draw()
	
	def calculate_oneway_time(self, distance, attacking_unit):
		return distance * self.unit_speeds[attacking_unit] / 60
	
	def calculate_distance(self, attacker_village_id, defender_village_id):
		attacker = self.sql.select(table="villages", param_list=('location_x', 'location_y'), where_param_dicts=({'field':'id', 'comparator':'=', 'value':attacker_village_id}, ), debug=False)
		att_x = attacker[0]['location_x']
		att_y = attacker[0]['location_y']
		
		defender = self.sql.select(table="villages", param_list=('location_x', 'location_y'), where_param_dicts=({'field':'id', 'comparator':'=', 'value':defender_village_id}, ), debug=False)
		def_x = defender[0]['location_x']
		def_y = defender[0]['location_y']
		
		return math.sqrt(math.pow(att_x - def_x, 2) + math.pow(att_y - def_y, 2))
	
	def delete_button_clicked(self, TODO_dunno):
		battle_id = self.sender().property('battle_id')
		self.sql._execute("JUST RUN IT", 'DELETE FROM battles WHERE id = %d' % battle_id, False)
		
		defender_village_id = self.sender().property('defender_village_id')
		self.sql._execute("JUST RUN IT", 'DELETE FROM villages WHERE id = %d' % defender_village_id, False)
		
		self.draw()
	
	def report_button_clicked(self, TODO_dunno):
		file_path = self.sender().property('file_path')
		webbrowser.open(file_path)
