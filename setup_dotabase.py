# @Author: DivineEnder
# @Date:   2017-05-18 18:58:14
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-05-18 23:48:48

import os
import sys
import json

from dotenv import find_dotenv, load_dotenv

from utils import settings
from utils import db_utils as db
from utils import connection_utils as glc

class Build(object):

	def __init__(self, static_json_dir = "ref/", build_plan = None, global_populate = True):
		load_dotenv(find_dotenv())

		self.static_json_dir = static_json_dir

		self.build_list = ["heroes", "items", "leaver", "lobbies", "modes", "regions", "abilities"]
		self.build_plan = { key: global_populate for key in self.build_list } if build_plan is None else build_plan

	@glc.new_connection(primary = True, pass_to_function = False)
	def build(self):
		for key in self.build_plan.keys():
			print("Building '%s' table..." % key)
			getattr(self, key)()
			if self.build_plan[key]:
				self.populate(key)

	def populate(self, table):
		data = json.load(open(self.static_json_dir + table + ".json", "r"))[table]

		for item in data:
			key_string = ",".join(["%s = EXCLUDED.%s" % (key, key) for key in item.keys() if not key == "id"])

			cols = [key for key in item.keys()]
			col_string = ""
			for i in range(0, len(cols)):
				col_string = col_string + cols[i]
				if i < len(cols) - 1:
					col_string = col_string + ","

			SQL_cmd = "INSERT INTO %s (%s) VALUES (" % (table, col_string)
			for i in range(0, len(item.keys())):
				SQL_cmd = SQL_cmd + "%s"
				if i < len(item.keys()) - 1:
					SQL_cmd = SQL_cmd + ","
			SQL_cmd = SQL_cmd + ") ON CONFLICT (id) DO UPDATE SET " + key_string

			glc.execute_db_values_command(SQL_cmd, tuple([item[col] for col in cols]))

	def heroes(self):
		glc.execute_db_command("""CREATE TABLE IF NOT EXISTS heroes (
			id bigint UNIQUE PRIMARY KEY,
			name varchar(100) NOT NULL,
			localized_name varchar(50) UNIQUE NOT NULL,
			url_full_portrait text NOT NULL,
			url_small_portrait text NOT NULL,
			url_large_portrait text NOT NULL,
			url_vertical_portrait text NOT NULL
		)""")

	def items(self):
		glc.execute_db_command("""CREATE TABLE IF NOT EXISTS items (
			id bigint UNIQUE PRIMARY KEY,
			name varchar(100) UNIQUE NOT NULL,
			localized_name varchar(50) NOT NULL,
			cost integer NOT NULL,
			recipe boolean NOT NULL,
			secret_shop boolean NOT NULL,
			side_shop boolean NOT NULL,
			url_image text NOT NULL
		)""")

	def leaver(self):
		glc.execute_db_command("""CREATE TABLE IF NOT EXISTS leaver (
			id bigint UNIQUE PRIMARY KEY,
			name varchar(50) NOT NULL,
			description text NOT NULL
		)""")

	def lobbies(self):
		glc.execute_db_command("""CREATE TABLE IF NOT EXISTS lobbies (
			id bigint UNIQUE PRIMARY KEY,
			name varchar(50) NOT NULL
		)""")

	def modes(self):
		glc.execute_db_command("""CREATE TABLE IF NOT EXISTS modes (
			id bigint UNIQUE PRIMARY KEY,
			name varchar(50) NOT NULL
		)""")

	def regions(self):
		glc.execute_db_command("""CREATE TABLE IF NOT EXISTS regions (
			id bigint UNIQUE PRIMARY KEY,
			name varchar(50) NOT NULL
		)""")

	def abilities(self):
		glc.execute_db_command("""CREATE TABLE IF NOT EXISTS abilities (
			id bigint UNIQUE PRIMARY KEY,
			name varchar(100) NOT NULL
		)""")

def main(args):
	builder = Build()
	builder.build()

if __name__ == "__main__":
	main(sys.argv[1:])
