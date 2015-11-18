#!/usr/bin/env python3.4
# -*- coding: utf8 -*-

# Copyright (C) 2015 Steffen Schaumburg and contributors, see docs/contributors.txt <steffen@schaumburger.info>
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
# In the original distribution you can find the license in docs/agpl_3.0.txt.


#python std lib
import datetime
import re
import sys

#mypy
#import typing

#PyQt modules
#from PyQt5.QtCore import QObject, Qt
#from PyQt5.QtSql import QSqlRelationalTableModel
#from PyQt5.QtWidgets import QLabel, QPushButton, QTextEdit

#own modules
from catlib.messenger import Messenger
from catlib.SQL_feeder import SQLFeeder
from user_settings import SQLFEEDER_BACKEND

class ReportParser(object):
	def __init__(self, msg, sql):
		self.sql = sql
		
		self.building_list = ('Hauptgebäude', 'Kaserne', 'Schmiede', 'Versammlungsplatz', 'Statue', 'Holzfällerlager', 'Lehmgrube', 'Eisenmine', 'Bauernhof', 'Speicher', 'Versteck', 'Wall') #TODO complete
		
		#2548->645steps e.g.: 		var game_data = {"player":{"id":"1576673594","name":"catpig","ally":"1777","sitter":"0","sleep_start":"0","sitter_type":"normal","sleep_end":"0","sleep_last":"0","interstitial":"0","email_valid":"1","villages":"1","incomings":"0","supports":0,"knight_location":"0","knight_unit":"261706559","rank":4836,"points":"609","date_started":"1444404131","is_guest":"0","birthdate":"0000-00-00","quest_progress":"0","premium":false,"account_manager":false,"farm_manager":false,"points_formatted":"609","rank_formatted":"4<span class=\"grey\">.<\/span>836","pp":"0","new_ally_application":"0","new_ally_invite":"0","new_buddy_request":"0","new_forum_post":"0","new_igm":"0","new_items":"0","new_report":"0","fire_pixel":"0","new_quest":"1"},"village":{"id":17329,"name":"Hollow Stump","wood_prod":0.074640683713199,"stone_prod":0.074640683713199,"iron_prod":0.086815925968678,"storage_max":7893,"pop_max":1002,"wood_float":416.70997458381,"stone_float":868.70997458381,"iron_float":1225.2299714095,"wood":417,"stone":869,"iron":1225,"pop":793,"x":603,"y":418,"trader_away":2,"bonus_id":null,"bonus":{"wood":1.08,"stone":1.08,"iron":1.08},"buildings":{"village":"17329","main":"10","farm":"10","storage":"11","place":"1","barracks":"5","church":"0","church_f":"0","smith":"5","wood":"15","stone":"15","iron":"16","market":"3","stable":"5","wall":"13","garage":"0","hide":"10","snob":"0","statue":"1","watchtower":"0"},"player_id":"1576673594","res":[417,0.074640683713199,869,0.074640683713199,1225,0.086815925968678,7893,793,1002],"coord":"603|418","is_farm_upgradable":true},"nav":{"parent":3},"link_base":"\/game.php?village=17329&amp;screen=","link_base_pure":"\/game.php?village=17329&screen=","csrf":"c322baf8","world":"de122","market":"de","RTL":false,"version":"27411 8.38","majorVersion":"8.38","screen":"report","mode":"all","device":"desktop","pregame":false,"time_generated":1445377695224};
		self.re_world_string = re.compile(r'var game_data = \{.*"world":"(?P<world_string>.*)","market', re.DOTALL)
		
		#228->80steps e.g.:						20.10.15 23:27:51<span class="small grey">:441</span>					</td>
		self.re_timestamp = re.compile(r'(?P<day>\d\d)\.(?P<month>\d\d)\.(?P<year>\d\d) (?P<hour>\d\d):(?P<minute>\d\d):(?P<second>\d\d)<span class="small grey">:(?P<millisecond>\d\d\d)</span>', re.DOTALL)
		
		#93->63steps e.g.:						    <h3>catpig hat gewonnen</h3>
		self.re_winner = re.compile(r'<h3>(?P<winning_player_name>.*) hat gewonnen</h3>', re.DOTALL)
		
		#TODOsteps e.g.:						    <h3>catpig hat Barbarendorf ausgekundschaftet</h3>
		self.re_spy_winner = re.compile(r'<h3>(?P<winning_player_name>.*) hat .* ausgekundschaftet</h3>', re.DOTALL)
		
		#32938>15482>1033steps e.g.:                                    <td style="text-align:center"  class='unit-item unit-item-spear hidden'>0</td><td style="text-align:center"  class='unit-item unit-item-sword hidden'>0</td><td style="text-align:center"  class='unit-item unit-item-axe hidden'>0</td><td style="text-align:center"  class='unit-item unit-item-archer hidden'>0</td><td style="text-align:center"  class='unit-item unit-item-spy hidden'>0</td><td style="text-align:center"  class='unit-item unit-item-light hidden'>0</td><td style="text-align:center"  class='unit-item unit-item-marcher hidden'>0</td><td style="text-align:center"  class='unit-item unit-item-heavy hidden'>0</td><td style="text-align:center"  class='unit-item unit-item-ram hidden'>0</td><td style="text-align:center"  class='unit-item unit-item-catapult hidden'>0</td><td style="text-align:center"  class='unit-item unit-item-knight hidden'>0</td><td style="text-align:center"  class='unit-item unit-item-snob hidden'>0</td><td style="text-align:center"  class='unit-item unit-item-militia hidden'>0</td>
		self.re_unit_counts = re.compile(r'unit-item-spear (hidden)?\'>(?P<spear>\d+)</td><td style="text-align:center"  class=\'unit-item unit-item-sword (hidden)?\'>(?P<sword>\d+)</td><td style="text-align:center"  class=\'unit-item unit-item-axe (hidden)?\'>(?P<axe>\d+)</td><td style="text-align:center"  class=\'unit-item unit-item-archer (hidden)?\'>(?P<archer>\d+)</td><td style="text-align:center"  class=\'unit-item unit-item-spy (hidden)?\'>(?P<scout>\d+)</td><td style="text-align:center"  class=\'unit-item unit-item-light (hidden)?\'>(?P<lcav>\d+)</td><td style="text-align:center"  class=\'unit-item unit-item-marcher (hidden)?\'>(?P<marcher>\d+)</td><td style="text-align:center"  class=\'unit-item unit-item-heavy (hidden)?\'>(?P<hcav>\d+)</td><td style="text-align:center"  class=\'unit-item unit-item-ram (hidden)?\'>(?P<ram>\d+)</td><td style="text-align:center"  class=\'unit-item unit-item-catapult (hidden)?\'>(?P<catapult>\d+)</td><td style="text-align:center"  class=\'unit-item unit-item-knight (hidden)?\'>(?P<paladin>\d+)</td><td style="text-align:center"  class=\'unit-item unit-item-snob (hidden)?\'>(?P<noblemen>\d+)</td>(<td style="text-align:center"  class=\'unit-item unit-item-militia (hidden)?\'>(?P<militia>\d+)</td>)?', re.DOTALL)
		
		#663wrong steps, 690->222steps e.g.:								<td width="250"><span class="nowrap"><span class="icon header wood" title="Holz"> </span>87</span> <span class="nowrap"><span class="icon header stone" title="Lehm"> </span>87</span> <span class="nowrap"><span class="icon header iron" title="Eisen"> </span>64</span> </td>
		self.re_loot = re.compile(r'icon header wood" title="Holz"> </span>(?P<wood>\d+)</span> <span class="nowrap"><span class="icon header stone" title="Lehm"> </span>(?P<clay>\d+)</span> <span class="nowrap"><span class="icon header iron" title="Eisen"> </span>(?P<iron>\d+)</span>', re.DOTALL)
		
		#120steps e.g.:	<th><a href="/game.php?village=17329&amp;screen=info_player&amp;id=1576673594"  title="#Jokers">catpig</a></th>
		self.re_player = re.compile(r'game\.php\?village=(?P<inno_village_id>\d+)&amp;screen=info_player&amp;id=(?P<inno_player_id>\d+).*>(?P<player_name>.*)<\/a>', re.DOTALL)
		
		#195steps e.g.:	<td><span class="village_anchor" data-player="0" data-id="16535"><a href="/game.php?village=17329&amp;screen=info_village&amp;id=16535" >Barbarendorf (596|416) K45</a></span></td>
		self.re_village = re.compile(r'"village_anchor" data-player="(?P<inno_player_id>\d+)" data-id="(?P<inno_village_id>\d+)"><a href="\/game\.php\?village=\d+&amp;screen=info_village&amp;id=\d+" >(?P<village_name>.+) \((?P<location_x>\d+)\|(?P<location_y>\d+)\) K\d+<\/a>', re.DOTALL)
		
		#293steps e.g.:                    <tr><th>Erspähte Rohstoffe:</th><td><span class="nowrap"><span class="icon header wood" title="Holz"> </span>136</span> <span class="nowrap"><span class="icon header stone" title="Lehm"> </span>158</span> <span class="nowrap"><span class="icon header iron" title="Eisen"> </span>100</span> </td></tr>
		self.re_spied_resources = re.compile(r'Erspähte Rohstoffe:<\/th><td>(<span class="nowrap"><span class="icon header wood" title="Holz"> <\/span>(?P<spied_wood>\d+)<\/span> )?(<span class="nowrap"><span class="icon header stone" title="Lehm"> <\/span>(?P<spied_clay>\d+)<\/span> )?(<span class="nowrap"><span class="icon header iron" title="Eisen"> <\/span>(?P<spied_iron>\d+)<\/span> )?<\/td><\/tr>', re.DOTALL)
		
		#29steps e.g.:                        <td class="middle">10 </td>
		self.re_building_level = re.compile(r'<td class="middle">(?P<building_level>\d+) <\/td>', re.DOTALL)
	
	def get_or_create_player_id(self, world_id, the_dict):
		#TODO update values if necessary? (e.g. name change)
		select_result = self.sql.select(table="players", param_list=("id", ), where_param_dicts=({'field':'inno_player_id', 'comparator':'=', 'value':the_dict['inno_player_id']}, ), debug=False)
		if select_result:
			player_id = select_result[0]['id']
		else:
			self.sql.insert(table='players', param_dict={'inno_player_id':the_dict['inno_player_id'], 'player_name':the_dict['player_name'], 'world_id':world_id}, debug=False) #TODO: tribe abbreviation
			player_id = self.sql.last_insert_id()
		
		return player_id
	
	def get_or_create_village_id(self, player_id, the_dict):
		#TODO update values if necessary? (e.g. owner change or conversion to barbarian)
		select_result = self.sql.select(table="villages", param_list=("id", ), where_param_dicts=({'field':'inno_village_id', 'comparator':'=', 'value':the_dict['inno_village_id']}, ), debug=False)
		if select_result:
			village_id = select_result[0]['id']
		else:
			self.sql.insert(table='villages', param_dict={'inno_village_id':the_dict['inno_village_id'], 'village_name':the_dict['village_name'], 'player_id':player_id, 'location_x':the_dict['location_x'], 'location_y':the_dict['location_y']}, debug=False) #TODO: tribe abbreviation
			village_id = self.sql.last_insert_id()
		
		return village_id
	
	def parse(self, input_whole, file_path_before_move, file_path_after_move):
		input_whole = input_whole.replace('<span class="grey">.</span>', '')
		dict_timestamp = None
		dict_winner = None
		dict_spy_winner = None
		dicts_unit_counts = []
		dict_loot = {'wood':None, 'clay':None, 'iron':None}
		dicts_players = []
		dicts_villages = []
		dict_spied_resources = {'spied_wood':None, 'spied_clay':None, 'spied_iron':None}
		
		dict_buildings = {}
		for building_name in self.building_list:
			dict_buildings[building_name] = None
		next_building = None
		found_a_building = False
		
		regex_start = datetime.datetime.now()
		for line in input_whole.split('\n'):
			m_world_string = self.re_world_string.search(line)
			m_timestamp = self.re_timestamp.search(line)
			m_winner = self.re_winner.search(line)
			m_spy_winner = self.re_spy_winner.search(line)
			m_unit_counts = self.re_unit_counts.search(line)
			m_loot = self.re_loot.search(line)
			m_player = self.re_player.search(line)
			m_village = self.re_village.search(line)
			m_spied_resources = self.re_spied_resources.search(line)
			
			if m_world_string is not None:
				world_string = m_world_string.groupdict()['world_string']
			if m_timestamp is not None:
				dict_timestamp = m_timestamp.groupdict()
			if m_winner is not None:
				dict_winner = m_winner.groupdict()
			if m_spy_winner is not None:
				dict_spy_winner = m_spy_winner.groupdict()
			if m_unit_counts is not None:
				dicts_unit_counts.append(m_unit_counts.groupdict())
			if m_loot is not None:
				dict_loot = m_loot.groupdict()
			if m_player is not None:
				dicts_players.append(m_player.groupdict())
			if m_village is not None:
				dicts_villages.append(m_village.groupdict())
			if m_spied_resources is not None:
				dict_spied_resources = m_spied_resources.groupdict()
			
			for building_name in self.building_list:
				if building_name in line:
					next_building = building_name
					break
			
			if next_building:
				m_building_level = self.re_building_level.search(line)
			
				if m_building_level is not None:
					dict_buildings[next_building] = m_building_level.groupdict()['building_level']
					next_building = None
					found_a_building = True
		
		#add barbarian if missing
		#print("dicts_villages", dicts_villages)
		if len(dicts_players) == 1:
			if dicts_villages[1]['village_name'] == 'Barbarendorf':
				dicts_players.append({'inno_village_id':dicts_villages[1]['inno_village_id'], 'inno_player_id':dicts_villages[1]['inno_player_id'], 'player_name':'Barbaren'})
			else:
				dicts_players = [{'inno_village_id':dicts_villages[1]['inno_village_id'], 'inno_player_id':dicts_villages[1]['inno_player_id'], 'player_name':'Barbaren'}, dicts_players[0]]
		
		#set unfound buildings to 0 if we found any building
		if found_a_building:
			for building_name in self.building_list:
				if dict_buildings[building_name] is None:
					dict_buildings[building_name] = 0
		
		#TODO set unfound spied res to 0 if we found any spied res
		
		#now get IDs
		world_id = self.sql.select(table="worlds", param_list=("id", ), where_param_dicts=({'field':'world_string', 'comparator':'=', 'value':world_string}, ), debug=False)[0]['id']
		#print("world_string", world_string, "world_id", world_id)
		
		#print("dicts_players", dicts_players)
		#print("dict_winner", dict_winner)
		#print("dict_spy_winner", dict_spy_winner)
		attacker_id = self.get_or_create_player_id(world_id, dicts_players[0])
		defender_id = self.get_or_create_player_id(world_id, dicts_players[1])
		if dict_winner:
			if dict_winner['winning_player_name'] == dicts_players[0]['player_name']:
				attacker_won = True
			elif dict_winner['winning_player_name'] == dicts_players[1]['player_name']:
				attacker_won = False
			else:
				print("TODO error dia: couldnt detect winner1")
				attacker_won = False
		elif dict_spy_winner:
			if dict_spy_winner['winning_player_name'] == dicts_players[0]['player_name']:
				attacker_won = True
			elif dict_spy_winner['winning_player_name'] == dicts_players[1]['player_name']:
				attacker_won = False
			else:
				print("TODO error dia: couldnt detect winner2")
				attacker_won = False
		else:
			print("TODO error dia: couldnt detect winner3")
			attacker_won = False
		#print("attacker_id", attacker_id, 'defender_id', defender_id, 'attacker_won', attacker_won)
		
		attacker_village_id = self.get_or_create_village_id(attacker_id, dicts_villages[0])
		defender_village_id = self.get_or_create_village_id(defender_id, dicts_villages[1])
		#print("attacker_village_id", attacker_village_id, 'defender_village_id', defender_village_id)
		
		#print("dict_timestamp", dict_timestamp)
		battle_ts = "20%s-%s-%s %s:%s:%s.%s" % (dict_timestamp['year'], dict_timestamp['month'], dict_timestamp['day'], dict_timestamp['hour'], dict_timestamp['minute'], dict_timestamp['second'], dict_timestamp['millisecond'])
		#print("battle_ts", battle_ts)
		
		#print("dicts_unit_counts", dicts_unit_counts)
		#print("dict_loot", dict_loot)
		#print("dict_spied_resources", dict_spied_resources)
		#print("dict_buildings", dict_buildings)
		
		#TODO in insert: 'stable':dict_buildings[''], 'workshop':dict_buildings[''], 'church':dict_buildings[''], 'first_church':dict_buildings[''], 'academy':dict_buildings[''], 'market':dict_buildings[''], 'attacker_luck':['']:[''], 'away_spears':['']:[''], 'away_archers':[''], 'away_scouts':[''], 'away_lcav':[''], 'away_mounted_archers':[''], 'away_hcav':[''], 'away_rams':[''], 'away_catapults':[''], 'away_paladin':[''], 'away_noblemen':['']
		
		select_result = self.sql.select(table="battles", param_list=("id", "battle_ts"), where_param_dicts=({'field':'defender_village_id', 'comparator':'=', 'value':defender_village_id}, {'field':'battle_ts', 'comparator':'>=', 'value':battle_ts}), debug=False)
		if select_result:
			print("skipping a file, as a report of equal age or newer is already in the DB")
		else:
			self.sql._execute("JUST RUN IT", 'DELETE FROM battles WHERE defender_village_id = %d AND battle_ts < "%s"' % (defender_village_id, battle_ts), False)
			
			self.sql.insert(table='battles', param_dict={'attacker_village_id':attacker_village_id, 'defender_village_id':defender_village_id, 'battle_ts':battle_ts, 'attacker_won':attacker_won, 'looted_wood':dict_loot['wood'], 'looted_clay':dict_loot['clay'], 'looted_iron':dict_loot['iron'], 'spied_wood':dict_spied_resources['spied_wood'], 'spied_clay':dict_spied_resources['spied_clay'], 'spied_iron':dict_spied_resources['spied_iron'], 'headquarters':dict_buildings['Hauptgebäude'], 'barracks':dict_buildings['Kaserne'], 'smithy':dict_buildings['Schmiede'], 'rally_point':dict_buildings['Versammlungsplatz'], 'statue':dict_buildings['Statue'], 'timber_camp':dict_buildings['Holzfällerlager'], 'clay_pit':dict_buildings['Lehmgrube'], 'iron_mine':dict_buildings['Eisenmine'], 'farm':dict_buildings['Bauernhof'], 'warehouse':dict_buildings['Speicher'], 'hiding_place':dict_buildings['Versteck'], 'wall':dict_buildings['Wall'], 'attacker_spears_sent':dicts_unit_counts[0]['spear'], 'attacker_swords_sent':dicts_unit_counts[0]['sword'], 'attacker_axes_sent':dicts_unit_counts[0]['axe'], 'attacker_archers_sent':dicts_unit_counts[0]['archer'], 'attacker_scouts_sent':dicts_unit_counts[0]['scout'], 'attacker_lcav_sent':dicts_unit_counts[0]['lcav'], 'attacker_mounted_archers_sent':dicts_unit_counts[0]['marcher'], 'attacker_hcav_sent':dicts_unit_counts[0]['hcav'], 'attacker_rams_sent':dicts_unit_counts[0]['ram'], 'attacker_catapults_sent':dicts_unit_counts[0]['catapult'], 'attacker_paladin_sent':dicts_unit_counts[0]['paladin'], 'attacker_noblemen_sent':dicts_unit_counts[0]['noblemen'], 'attacker_spears_lost':dicts_unit_counts[1]['spear'], 'attacker_swords_lost':dicts_unit_counts[1]['sword'], 'attacker_axes_lost':dicts_unit_counts[1]['axe'], 'attacker_archers_lost':dicts_unit_counts[1]['archer'], 'attacker_scouts_lost':dicts_unit_counts[1]['scout'], 'attacker_lcav_lost':dicts_unit_counts[1]['lcav'], 'attacker_mounted_archers_lost':dicts_unit_counts[1]['marcher'], 'attacker_hcav_lost':dicts_unit_counts[1]['hcav'], 'attacker_rams_lost':dicts_unit_counts[1]['ram'], 'attacker_catapults_lost':dicts_unit_counts[1]['catapult'], 'attacker_paladin_lost':dicts_unit_counts[1]['paladin'], 'attacker_noblemen_lost':dicts_unit_counts[1]['noblemen'], 'defender_spears_sent':dicts_unit_counts[2]['spear'], 'defender_swords_sent':dicts_unit_counts[2]['sword'], 'defender_axes_sent':dicts_unit_counts[2]['axe'], 'defender_archers_sent':dicts_unit_counts[2]['archer'], 'defender_scouts_sent':dicts_unit_counts[2]['scout'], 'defender_lcav_sent':dicts_unit_counts[2]['lcav'], 'defender_mounted_archers_sent':dicts_unit_counts[2]['marcher'], 'defender_hcav_sent':dicts_unit_counts[2]['hcav'], 'defender_rams_sent':dicts_unit_counts[2]['ram'], 'defender_catapults_sent':dicts_unit_counts[2]['catapult'], 'defender_paladin_sent':dicts_unit_counts[2]['paladin'], 'defender_noblemen_sent':dicts_unit_counts[2]['noblemen'], 'defender_militia_sent':dicts_unit_counts[2]['militia'], 'defender_spears_lost':dicts_unit_counts[3]['spear'], 'defender_swords_lost':dicts_unit_counts[3]['sword'], 'defender_axes_lost':dicts_unit_counts[3]['axe'], 'defender_archers_lost':dicts_unit_counts[3]['archer'], 'defender_scouts_lost':dicts_unit_counts[3]['scout'], 'defender_lcav_lost':dicts_unit_counts[3]['lcav'], 'defender_mounted_archers_lost':dicts_unit_counts[3]['marcher'], 'defender_hcav_lost':dicts_unit_counts[3]['hcav'], 'defender_rams_lost':dicts_unit_counts[3]['ram'], 'defender_catapults_lost':dicts_unit_counts[3]['catapult'], 'defender_paladin_lost':dicts_unit_counts[3]['paladin'], 'defender_noblemen_lost':dicts_unit_counts[3]['noblemen'], 'defender_militia_lost':dicts_unit_counts[3]['militia'], 'file_path_before_move':file_path_before_move, 'file_path_after_move':file_path_after_move}, debug=False)
		

if __name__ == '__main__':
	msg = Messenger(None, "pytw", False)
	sql = SQLFeeder(msg, SQLFEEDER_BACKEND, 'pytw')
	report_parser = ReportParser(msg, sql)
	
	with open(sys.argv[1], 'r') as infile:
		print("importing", sys.argv[1])
		report_parser.parse(infile.read(), sys.argv[1])
	
	sys.exit(0)
