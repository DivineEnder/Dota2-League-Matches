# @Author: DivineEnder <DivineHP>
# @Date:   2017-03-04 23:42:57
# @Last modified by:   DivineEnder
# @Last modified time: 2017-05-18 22:49:08 

import os
import psycopg2
from functools import wraps
import utils.connection_utils as glc

# --------------------
# | GENERIC DB UTILS |
# --------------------

def list_all_db_tables(cursor = None):
	print("Possible tables are: ")
	print(glc.execute_db_query("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';", cursor = cursor))

def close_all_db_connections(dbname = os.environ.get("DBNAME"), connection = None, cursor = None):
	glc.execute_db_command("""SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = %s AND pid <> pg_backend_pid();""", (dbname,), connection = connection, cursor = cursor)

def add_table_to_db(table_name, *cols, connection = None, cursor = None, VERBOSE = False):
	cols_string = ""
	for col in cols:
		cols_string = cols_string + col + ", "
	cols_string = cols_string[0:-2]

	glc.execute_db_command("""CREATE TABLE %s (%s)""", (table_name, cols_string), connection = connection, cursor = cursor)

	if VERBOSE:
		print("Added %d table with columns: ")
		for col in cols:
			print("  %s" % col)

# def add_table_to_db_from_dict(table_name, dict, connection = None, cursor = None, VERBOSE = False):
# 	SQL_cmd = "CREATE TABLE %s (" % table_name
# 	for key in dict.keys():
# 		field_type = text
# 		if key == "id":
# 			field_type = "bigint"
# 		elif isinstance(key, str):
# 			if len(key) < 255:
#
# 		SQL_cmd = SQL_cmd + "%s %s NOT NULL" % (key, field_type)
# 	# add_table_to_db(table_name, *[key for key in dict.keys()], connection = connection, cursor = cursor, VERBOSE = VERBOSE)

# def upsert_dict_into_table(table, dict, connection = None, cursor = None, VERBOSE = False):
# 	key_string = ",".join(["%s = EXCLUDED.%s" % (key, key) for key in dict.keys() if not key == "id"])
#
# 	SQL_cmd = "INSERT INTO %s VALUES (" % table
# 	for i in range(0, len(dict.keys()) - 1):
# 		SQL_cmd = SQL_cmd + "%s"
# 		if i < len(dict.keys()) - 2):
# 			SQL_cmd = SQL_cmd + ","
# 	SQL_cmd = SQL_cmd + ") ON CONFLICT (id) DO UPDATE SET " + key_string
#
# 	print(SQL_cmd % tuple(list([key for key in dict.keys() if not key == "id"])))

def add_column_to_table(table, col_name, col_type, connection = None, cursor = None, VERBOSE = False):
	glc.execute_db_command("""ALTER TABLE %s ADD COLUMN %s %s""", (table, col_name, col_type))

	if VERBOSE:
		print("Added column %s to %s table [type:%s]." % (table, col_name, col_type))

def drop_column_from_table(table, col_name, connection = None, cursor = None, VERBOSE = False):
	glc.execute_db_command("""ALTER TABLE %s DROP COLUMN %s""", (table, col_name), connection = connection, cursor = cursor)

	if VERBOSE:
		print("Dropped column %s from %s table." % (col_name, table))

def set_column_default(table, col_name, default_val, connection = None, cursor = None, VERBOSE = False):
	glc.execute_db_command("""ALTER TABLE %s ALTER COLUMN %s SET DEFAULT %s""", (table, col_name, default_val), connection = connection, cursor = cursor)

	if VERBOSE:
		print("Set default for %s in %s table to %s." % (col_name, table, default_val))

def drop_column_default(table, col_name, connection = None, cursor = None, VERBOSE = False):
	glc.execute_db_command("""ALTER TABLE %s ALTER COLUMN DROP DEFAULT""", (table, col_name), connection = connection, cursor = cursor)

	if VERBOSE:
		print("Dropped default for %s in %s table.")

def drop_constraint_from_table(table, cons_name, connection = None, cursor = None, VERBOSE = False):
	glc.execute_db_command("""ALTER TABLE %s DROP CONSTRAINT %s""", (table, cons_name), connection = connection, cursor = cursor)

	if VERBOSE:
		print("Dropped %s constraint from %s table" % (cons_name, table))

# --------------------
# | GENERIC DB UTILS |
# --------------------
