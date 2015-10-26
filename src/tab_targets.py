# -*- coding: utf8 -*-

# Copyright (C) 2015 Steffen Schaumburg and contributors, see docs/contributors.txt <steffen@schaumburger.info>
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
# In the original distribution you can find the license in docs/agpl_3.0.txt.

#python stdlib
import datetime
import math

#mypy
#import typing

#PyQt modules
#from PyQt5.QtCore import QObject, Qt
#from PyQt5.QtSql import QSqlRelationalTableModel
from PyQt5.QtWidgets import QComboBox, QLabel, QPushButton, QTextEdit

#own modules
from catlib.grid_scroll_tab import GridScrollTab

class TabTargets(GridScrollTab):
	def __init__(self, msg, sql):
		super(TabTargets, self).__init__()
		self.name = "Targets"
		self.msg = msg
		self.sql = sql
		self.headers = ("village_name", "battle_ts", "location_x", "location_y", "dist", "sword", "spear", "lcav", "scout", "delete")
		self.unit_speeds = {"sword":22, "spear":18, "lcav":10, "scout":9}
		self.combo_barbarian = None
		self.draw()
	
	def draw(self):
		if self.combo_barbarian:
			combo_barbarian_old_setting = self.combo_barbarian.currentIndex()
		else:
			combo_barbarian_old_setting = 0
		
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
		current_y += 1
		
		for header in self.headers:
			if header in ("sword", "spear", "lcav", "scout"):
				self.layout.addWidget(QLabel("attack with"), current_y, current_x, 1, 1)
			elif header in ("battle_ts"):
				self.layout.addWidget(QLabel("report_time"), current_y, current_x, 1, 1)
			else:
				self.layout.addWidget(QLabel(header), current_y, current_x, 1, 1)
			current_x += 1
		current_y += 1
		current_x = 0
		
		where_param_dicts = []
		for field in ('wall', 'defender_spears_sent', 'defender_swords_sent', 'defender_axes_sent', 'defender_archers_sent', 'defender_scouts_sent', 'defender_lcav_sent', 'defender_mounted_archers_sent', 'defender_hcav_sent', 'defender_rams_sent', 'defender_catapults_sent', 'defender_paladin_sent', 'defender_nobleman_sent', 'defender_militia_sent'):
			where_param_dicts.append({'field':field, 'comparator':'=', 'value':0})
		
		if self.combo_barbarian.currentIndex() == 0:
			where_literal = 'AND village_name != "Barbarendorf" AND village_name != "Bonusdorf"'
		elif self.combo_barbarian.currentIndex() == 1:
			where_literal = 'AND (village_name = "Barbarendorf" OR village_name = "Bonusdorf")'
		else:
			where_literal = ''
		
		targets = self.sql.select(table="battles INNER JOIN villages ON battles.defender_village_id = villages.id", param_list=('location_x', 'location_y', 'village_name', 'battle_ts', 'spied_wood', 'spied_clay', 'spied_iron', 'timber_camp', 'clay_pit', 'iron_mine', 'attacker_village_id', 'defender_village_id', 'battles.id'), where_param_dicts=where_param_dicts, where_literal=where_literal, debug=False)
		
		for target in targets:
			is_current_attack_target = self.sql.select(table="scheduled_attacks", param_list=('defender_village_id', ), where_param_dicts=({'field':'defender_village_id', 'comparator':'=', 'value':target['defender_village_id']}, {'field':'arrival_ts', 'comparator':'>', 'value':"'"+str(datetime.datetime.now())+"'"}), debug=False)
			if is_current_attack_target:
				continue
			
			delta_hours = (datetime.datetime.now() - datetime.datetime.strptime(target['battle_ts'], '%Y-%m-%d %H:%M:%S.%f')).seconds/3600
			target["dist"] = self.calculate_distance(target['attacker_village_id'], target['defender_village_id'])
			
			if type(target['spied_wood']) == str:
				target['spied_wood'] = 0
			if type(target['spied_clay']) == str:
				target['spied_clay'] = 0
			if type(target['spied_iron']) == str:
				target['spied_iron'] = 0
			
			for field in self.headers:
				if field in ("sword", "spear", "lcav", "scout"):
					oneway_time = self.calculate_oneway_time(target["dist"], field)
					wood = target['spied_wood'] + round(48 * math.pow(1.163118, target['timber_camp']-1) / 1.6 * (delta_hours + oneway_time))
					clay = target['spied_clay'] + round(48 * math.pow(1.163118, target['clay_pit']-1) / 1.6 * (delta_hours + oneway_time))
					iron = target['spied_iron'] + round(48 * math.pow(1.163118, target['iron_mine']-1) / 1.6 * (delta_hours + oneway_time))
					expected_loot = wood + clay + iron
					
					button = QPushButton(field + str(expected_loot))
					button.setProperty('attacker_village_id', target['attacker_village_id'])
					button.setProperty('defender_village_id', target['defender_village_id'])
					button.setProperty('attacking_unit', field)
					button.setProperty('oneway_time', oneway_time)
					button.clicked.connect(self.attack_button_clicked)
					self.layout.addWidget(button, current_y, current_x, 1, 1)
				elif field == "delete":
					button = QPushButton(field)
					button.setProperty('battle_id', target['battles.id'])
					button.setProperty('defender_village_id', target['defender_village_id'])
					button.clicked.connect(self.delete_button_clicked)
					self.layout.addWidget(button, current_y, current_x, 1, 1)
				elif field == "dist":
					self.layout.addWidget(QLabel('%.1f' % target[field]), current_y, current_x, 1, 1)
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
