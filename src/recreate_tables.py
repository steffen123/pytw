#!/usr/bin/env python3.4
# -*- coding: utf8 -*-

# Copyright (C) 2015 Steffen Schaumburg and contributors, see docs/contributors.txt <steffen@schaumburger.info>
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
# In the original distribution you can find the license in docs/agpl_3.0.txt.

#python std lib
from datetime import datetime
import os
import sys

#other 3rd party libs
#import typing

#own modules
from constants import DB_VERSION
from catlib.messenger import Messenger
from catlib.SQL_feeder import SQLFeeder
from user_settings import SQLFEEDER_BACKEND

class RecreateTables():
	def __init__(self) -> None:
		self.messenger = Messenger(args=None, name="pytw", has_GUI=False)
		self.sql = SQLFeeder(self.messenger, SQLFEEDER_BACKEND, 'pytw')
		
		table = (
			{'not_null':True, 'name':'id', 'type':'VARCHAR(100)'},
			{'not_null':True, 'name':'value', 'type':'VARCHAR(100)'},
		)
		self.sql.create_table('general', "general things", table, False)
		self.sql.insert('general', {'id':'schema_version', 'value':DB_VERSION})
		self.sql.insert('general', {'id':'db_create_ts', 'value':datetime.now()})
		with open(os.path.join('src', 'version.ini'), 'r') as infile:
			self.sql.insert('general', {'id':'created_with_tool_version', 'value':infile.readlines()[0][:-1]})
		
		#TODO change most not_null to True
		table = (
			{'not_null':True, 'name':'id', 'type':'PKEY'},
			{'not_null':True, 'name':'world_string', 'type':'VARCHAR(10)'},
			
			#settings
			{'not_null':False, 'name':'game_speed', 'type':'INT16', 'comment':'in thousanths seconds'},
			{'not_null':False, 'name':'unit_speed', 'type':'INT16', 'comment':'in thousanths seconds'},
			{'not_null':False, 'name':'demolish_buildings', 'type':'BOOLEAN'},
			{'not_null':False, 'name':'morale', 'type':'VARCHAR(12)', 'comment':'valid values: no, time, not time'},
			{'not_null':False, 'name':'farm_rule', 'type':'BOOLEAN'},
			
			{'not_null':False, 'name':'basic_defense', 'type':'INT16'},
			{'not_null':False, 'name':'milliseconds', 'type':'INT16'},
			{'not_null':False, 'name':'fake_limit', 'type':'INT16', 'comment':'in permille (ie 1%=10)'},
			{'not_null':False, 'name':'research_system', 'type':'VARCHAR(12)', 'comment':'valid values: simple, 3-level'},
			{'not_null':False, 'name':'church', 'type':'BOOLEAN'},
			
			{'not_null':False, 'name':'achievements', 'type':'BOOLEAN'},
			{'not_null':False, 'name':'barbarian_villages_grow_to', 'type':'INT16', 'comment':'0 means no growth, else it is the point value'},
			{'not_null':False, 'name':'bonus_villages', 'type':'VARCHAR(12)', 'comment':'valid values: none, simple, enhanced'},
			{'not_null':False, 'name':'cancel_attack_time', 'type':'INT16', 'comment':'in seconds'},
			{'not_null':False, 'name':'cancel_trade_time', 'type':'INT16', 'comment':'in seconds'},
			
			{'not_null':False, 'name':'night_bonus_from', 'type':'INT32', 'comment':'in seconds after 0:00'},
			{'not_null':False, 'name':'night_bonus_to', 'type':'INT32', 'comment':'in seconds after 0:00'},
			{'not_null':False, 'name':'beginner_protection', 'type':'INT32', 'comment':'in seconds'},
			{'not_null':False, 'name':'max_att_def_ratio', 'type':'INT16'},
			{'not_null':False, 'name':'max_att_def_ratio_for', 'type':'INT16', 'comment':'in days'},
			{'not_null':False, 'name':'casual_attack_block_percent', 'type':'INT16'},
			{'not_null':False, 'name':'flags', 'type':'BOOLEAN'},
			
			#units
			{'not_null':False, 'name':'archers', 'type':'BOOLEAN'},
			{'not_null':False, 'name':'scout_system', 'type':'VARCHAR(12)', 'comment':'valid values: normal, with foreign'},
			{'not_null':False, 'name':'paladin', 'type':'BOOLEAN'},
			{'not_null':False, 'name':'paladin_weapons', 'type':'BOOLEAN'},
			{'not_null':False, 'name':'paladin_weapons_improvement', 'type':'BOOLEAN'},
			{'not_null':False, 'name':'militia', 'type':'BOOLEAN'},
			
			#noblemen
			{'not_null':False, 'name':'noble_price_increase', 'type':'VARCHAR(12)', 'comment':'valid values: gold'},
			{'not_null':False, 'name':'noblemen_distance', 'type':'INT16'},
			{'not_null':False, 'name':'noblemen_attack_min', 'type':'INT16'},
			{'not_null':False, 'name':'noblemen_attack_max', 'type':'INT16'},
			{'not_null':False, 'name':'loyalty_per_hour', 'type':'INT16'},
			
			#configuration
			{'not_null':False, 'name':'tribe_member_limit', 'type':'INT16'},
			{'not_null':False, 'name':'defeated_oponent_rankings', 'type':'VARCHAR(12)', 'comment':'valid values: by points'},
			{'not_null':False, 'name':'account_sitting', 'type':'BOOLEAN'},
			{'not_null':False, 'name':'account_sitting_restriction', 'type':'VARCHAR(200)'},
			{'not_null':False, 'name':'free_trade', 'type':'VARCHAR(200)'},
			
			{'not_null':False, 'name':'select_direction', 'type':'BOOLEAN'},
			{'not_null':False, 'name':'victory_requirements', 'type':'VARCHAR(200)'},
			{'not_null':False, 'name':'start_date', 'type':'DATETIME'},
			{'not_null':False, 'name':'version', 'type':'VARCHAR(20)'},
			{'not_null':False, 'name':'data_ts', 'type':'DATETIME'},
		)
		self.sql.create_table('worlds', "TODO", table, False)
		
		table = (
			{'not_null':True, 'name':'id', 'type':'PKEY'},
			{'not_null':True, 'name':'world_id', 'type':'FKEY', 'fkey_table':'worlds'},
			{'not_null':True, 'name':'alarm_ts', 'type':'DATETIME'},
			{'not_null':True, 'name':'completed', 'type':'BOOLEAN', 'default':False},
			{'not_null':True, 'name':'importance', 'type':'INT16'},
			{'not_null':True, 'name':'user_note', 'type':'VARCHAR(500)'},
		)
		self.sql.create_table('alarms', "TODO", table, False)
		
		table = (
			{'not_null':True, 'name':'id', 'type':'PKEY'},
			{'not_null':True, 'name':'world_id', 'type':'FKEY', 'fkey_table':'worlds'},
			{'not_null':True, 'name':'inno_player_id', 'type':'INT64'},
			{'not_null':True, 'name':'player_name', 'type':'VARCHAR(100)'},
			{'not_null':False, 'name':'last_activity_detected_ts', 'type':'DATETIME'},
			{'not_null':False, 'name':'tribe_abbreviation', 'type':'VARCHAR(100)'},
			{'not_null':False, 'name':'current_score', 'type':'INT32'},
			{'not_null':False, 'name':'data_ts', 'type':'DATETIME'},
			{'not_null':False, 'name':'max_known_flag_attack_strength', 'type':'INT16'}, #TODO change not_null to True on this
			{'not_null':False, 'name':'max_known_flag_defense_strength', 'type':'INT16'}, #TODO change not_null to True on this
			{'not_null':False, 'name':'max_known_flag_loot_capacity', 'type':'INT16'}, #TODO change not_null to True on this
		)
		self.sql.create_table('players', "TODO", table, False)
		
		table = (
			{'not_null':True, 'name':'id', 'type':'PKEY'},
			{'not_null':True, 'name':'player_id', 'type':'FKEY', 'fkey_table':'players'},
			{'not_null':True, 'name':'continent', 'type':'VARCHAR(4)'},
			{'not_null':True, 'name':'score', 'type':'INT32'},
			{'not_null':False, 'name':'continent_score', 'type':'INT32'},
			{'not_null':True, 'name':'rank', 'type':'INT32'},
			{'not_null':False, 'name':'continent_rank', 'type':'INT32'},
			{'not_null':True, 'name':'village_count', 'type':'INT32'},
			{'not_null':True, 'name':'source', 'type':'INT32'},
			{'not_null':True, 'name':'data_ts', 'type':'DATETIME'},
		)
		self.sql.create_table('player_rankings', "TODO", table, False)
		
		table = (
			{'not_null':True, 'name':'id', 'type':'PKEY'},
			{'not_null':True, 'name':'inno_village_id', 'type':'INT64'},
			{'not_null':True, 'name':'player_id', 'type':'FKEY', 'fkey_table':'player'},
			{'not_null':True, 'name':'village_name', 'type':'VARCHAR(100)'},
			{'not_null':True, 'name':'location_x', 'type':'INT16'},
			{'not_null':True, 'name':'location_y', 'type':'INT16'},
			{'not_null':False, 'name':'current_score', 'type':'INT32'},
			{'not_null':False, 'name':'data_ts', 'type':'DATETIME'},
		)
		self.sql.create_table('villages', "TODO", table, False)
		
		table = (
			{'not_null':True, 'name':'id', 'type':'PKEY'},
			{'not_null':True, 'name':'village_id', 'type':'FKEY', 'fkey_table':'villages'},
			{'not_null':True, 'name':'continent', 'type':'VARCHAR(4)'},
			{'not_null':True, 'name':'score', 'type':'INT32'},
			{'not_null':True, 'name':'rank', 'type':'INT32'},
			{'not_null':False, 'name':'continent_rank', 'type':'INT32'},
			{'not_null':True, 'name':'source', 'type':'VARCHAR(20)', 'comment':'one of: map, report, ranking'},
			{'not_null':True, 'name':'data_ts', 'type':'DATETIME'},
		)
		self.sql.create_table('village_rankings', "TODO", table, False)
		
		table = (
			{'not_null':True, 'name':'id', 'type':'PKEY'},
			{'not_null':True, 'name':'attacker_village_id', 'type':'FKEY', 'fkey_table':'villages'},
			{'not_null':True, 'name':'defender_village_id', 'type':'FKEY', 'fkey_table':'villages'},
			{'not_null':True, 'name':'is_attack', 'type':'BOOLEAN', 'comment':'TRUE means attack, FALSE means support'},
			{'not_null':True, 'name':'slowest_unit', 'type':'VARCHAR(10)'},
			{'not_null':True, 'name':'launch_ts', 'type':'DATETIME'},
			{'not_null':True, 'name':'arrival_ts', 'type':'DATETIME'},
			{'not_null':True, 'name':'return_ts', 'type':'DATETIME'},
		)
		self.sql.create_table('scheduled_attacks', "TODO", table, False)
		
		table = (
			{'not_null':True, 'name':'id', 'type':'PKEY'},
			{'not_null':True, 'name':'file_path_before_move', 'type':'VARCHAR(500)'},
			{'not_null':True, 'name':'file_path_after_move', 'type':'VARCHAR(500)'},
			{'not_null':True, 'name':'attacker_village_id', 'type':'FKEY', 'fkey_table':'villages'},
			{'not_null':True, 'name':'defender_village_id', 'type':'FKEY', 'fkey_table':'villages'},
			{'not_null':True, 'name':'battle_ts', 'type':'DATETIME'},
			
			{'not_null':False, 'name':'has_latest_resources', 'type':'BOOLEAN'}, #TODO change not_null to True on this
			{'not_null':True, 'name':'has_latest_units', 'type':'BOOLEAN'},
			{'not_null':False, 'name':'has_latest_flag', 'type':'BOOLEAN'}, #TODO change not_null to True on this
			{'not_null':True, 'name':'has_latest_buildings', 'type':'BOOLEAN'},
			{'not_null':False, 'name':'has_latest_away_units', 'type':'BOOLEAN'}, #TODO change not_null to True on this
			
			{'not_null':False, 'name':'flag_attack_strength', 'type':'INT16'}, #TODO change not_null to True on this
			{'not_null':False, 'name':'flag_defense_strength', 'type':'INT16'}, #TODO change not_null to True on this
			{'not_null':False, 'name':'flag_loot_capacity', 'type':'INT16'}, #TODO change not_null to True on this
			
			{'not_null':True, 'name':'attacker_won', 'type':'BOOLEAN'},
			{'not_null':False, 'name':'looted_wood', 'type':'INT32'},
			{'not_null':False, 'name':'looted_clay', 'type':'INT32'},
			{'not_null':False, 'name':'looted_iron', 'type':'INT32'},
			{'not_null':False, 'name':'spied_wood', 'type':'INT32'},
			{'not_null':False, 'name':'spied_clay', 'type':'INT32'},
			{'not_null':False, 'name':'spied_iron', 'type':'INT32'},
			
			{'not_null':False, 'name':'headquarters', 'type':'INT16'},
			{'not_null':False, 'name':'barracks', 'type':'INT16'},
			{'not_null':False, 'name':'stable', 'type':'INT16'},
			{'not_null':False, 'name':'workshop', 'type':'INT16'},
			{'not_null':False, 'name':'church', 'type':'INT16'},
			{'not_null':False, 'name':'first_church', 'type':'INT16'},
			{'not_null':False, 'name':'academy', 'type':'INT16'},
			{'not_null':False, 'name':'smithy', 'type':'INT16'},
			{'not_null':False, 'name':'rally_point', 'type':'INT16'},
			{'not_null':False, 'name':'statue', 'type':'INT16'},
			{'not_null':False, 'name':'market', 'type':'INT16'},
			{'not_null':False, 'name':'timber_camp', 'type':'INT16'},
			{'not_null':False, 'name':'clay_pit', 'type':'INT16'},
			{'not_null':False, 'name':'iron_mine', 'type':'INT16'},
			{'not_null':False, 'name':'farm', 'type':'INT16'},
			{'not_null':False, 'name':'warehouse', 'type':'INT16'},
			{'not_null':False, 'name':'hiding_place', 'type':'INT16'},
			{'not_null':False, 'name':'wall', 'type':'INT16'},
			
			{'not_null':False, 'name':'ram_damage', 'type':'INT16', 'comment':'number of levels taken'},
			{'not_null':False, 'name':'catapult_target', 'type':'VARCHAR(30)'},
			{'not_null':False, 'name':'catapult_damage', 'type':'INT16', 'comment':'number of levels taken'},
			
			{'not_null':False, 'name':'attacker_luck', 'type':'INT16'}, #TODO no not_null
			{'not_null':False, 'name':'morale', 'type':'INT16'},
			
			{'not_null':False, 'name':'away_spears', 'type':'INT32'},
			{'not_null':False, 'name':'away_swords', 'type':'INT32'},
			{'not_null':False, 'name':'away_axes', 'type':'INT32'},
			{'not_null':False, 'name':'away_archers', 'type':'INT32'},
			{'not_null':False, 'name':'away_scouts', 'type':'INT32'},
			{'not_null':False, 'name':'away_lcav', 'type':'INT32'},
			{'not_null':False, 'name':'away_mounted_archers', 'type':'INT32'},
			{'not_null':False, 'name':'away_hcav', 'type':'INT32'},
			{'not_null':False, 'name':'away_rams', 'type':'INT32'},
			{'not_null':False, 'name':'away_catapults', 'type':'INT32'},
			{'not_null':False, 'name':'away_paladin', 'type':'INT32'},
			{'not_null':False, 'name':'away_noblemen', 'type':'INT32'},
			
			{'not_null':False, 'name':'attacker_spears_sent', 'type':'INT32'},
			{'not_null':False, 'name':'attacker_swords_sent', 'type':'INT32'},
			{'not_null':False, 'name':'attacker_axes_sent', 'type':'INT32'},
			{'not_null':False, 'name':'attacker_archers_sent', 'type':'INT32'},
			{'not_null':False, 'name':'attacker_scouts_sent', 'type':'INT32'},
			{'not_null':False, 'name':'attacker_lcav_sent', 'type':'INT32'},
			{'not_null':False, 'name':'attacker_mounted_archers_sent', 'type':'INT32'},
			{'not_null':False, 'name':'attacker_hcav_sent', 'type':'INT32'},
			{'not_null':False, 'name':'attacker_rams_sent', 'type':'INT32'},
			{'not_null':False, 'name':'attacker_catapults_sent', 'type':'INT32'},
			{'not_null':False, 'name':'attacker_paladin_sent', 'type':'INT32'},
			{'not_null':False, 'name':'attacker_paladin_weapon', 'type':'VARCHAR(50)'},
			{'not_null':False, 'name':'attacker_noblemen_sent', 'type':'INT32'},
			
			{'not_null':False, 'name':'attacker_spears_lost', 'type':'INT32'},
			{'not_null':False, 'name':'attacker_swords_lost', 'type':'INT32'},
			{'not_null':False, 'name':'attacker_axes_lost', 'type':'INT32'},
			{'not_null':False, 'name':'attacker_archers_lost', 'type':'INT32'},
			{'not_null':False, 'name':'attacker_scouts_lost', 'type':'INT32'},
			{'not_null':False, 'name':'attacker_lcav_lost', 'type':'INT32'},
			{'not_null':False, 'name':'attacker_mounted_archers_lost', 'type':'INT32'},
			{'not_null':False, 'name':'attacker_hcav_lost', 'type':'INT32'},
			{'not_null':False, 'name':'attacker_rams_lost', 'type':'INT32'},
			{'not_null':False, 'name':'attacker_catapults_lost', 'type':'INT32'},
			{'not_null':False, 'name':'attacker_paladin_lost', 'type':'INT32'},
			{'not_null':False, 'name':'attacker_noblemen_lost', 'type':'INT32'},
			
			{'not_null':False, 'name':'defender_spears_sent', 'type':'INT32'},
			{'not_null':False, 'name':'defender_swords_sent', 'type':'INT32'},
			{'not_null':False, 'name':'defender_axes_sent', 'type':'INT32'},
			{'not_null':False, 'name':'defender_archers_sent', 'type':'INT32'},
			{'not_null':False, 'name':'defender_scouts_sent', 'type':'INT32'},
			{'not_null':False, 'name':'defender_lcav_sent', 'type':'INT32'},
			{'not_null':False, 'name':'defender_mounted_archers_sent', 'type':'INT32'},
			{'not_null':False, 'name':'defender_hcav_sent', 'type':'INT32'},
			{'not_null':False, 'name':'defender_rams_sent', 'type':'INT32'},
			{'not_null':False, 'name':'defender_catapults_sent', 'type':'INT32'},
			{'not_null':False, 'name':'defender_paladin_sent', 'type':'INT32'},
			{'not_null':False, 'name':'defender_paladin_weapon', 'type':'VARCHAR(50)'},
			{'not_null':False, 'name':'defender_noblemen_sent', 'type':'INT32'},
			{'not_null':False, 'name':'defender_militia_sent', 'type':'INT32'},
			
			{'not_null':False, 'name':'defender_spears_lost', 'type':'INT32'},
			{'not_null':False, 'name':'defender_swords_lost', 'type':'INT32'},
			{'not_null':False, 'name':'defender_axes_lost', 'type':'INT32'},
			{'not_null':False, 'name':'defender_archers_lost', 'type':'INT32'},
			{'not_null':False, 'name':'defender_scouts_lost', 'type':'INT32'},
			{'not_null':False, 'name':'defender_lcav_lost', 'type':'INT32'},
			{'not_null':False, 'name':'defender_mounted_archers_lost', 'type':'INT32'},
			{'not_null':False, 'name':'defender_hcav_lost', 'type':'INT32'},
			{'not_null':False, 'name':'defender_rams_lost', 'type':'INT32'},
			{'not_null':False, 'name':'defender_catapults_lost', 'type':'INT32'},
			{'not_null':False, 'name':'defender_paladin_lost', 'type':'INT32'},
			{'not_null':False, 'name':'defender_noblemen_lost', 'type':'INT32'},
			{'not_null':False, 'name':'defender_militia_lost', 'type':'INT32'},
		)
		self.sql.create_table('battles', "TODO", table, False)
		
		self.messenger.message_debug("finished RecreateTables")

if __name__ == '__main__':
	muh = RecreateTables()
	sys.exit(0)
