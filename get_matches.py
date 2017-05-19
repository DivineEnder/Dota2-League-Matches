# @Author: DivineEnder
# @Date:   2017-05-18 17:53:36
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-05-19 12:39:51


import os
import sys
import json
from pprint import pprint

import dota2api
from dotenv import find_dotenv, load_dotenv

def main(args):
	api = dota2api.Initialise(os.environ.get("STEAM_API_KEY"))

	# hist = api.get_match_history(account_id = 76561198037873340)
	# pprint(hist, indent = 2, stream = open("test.txt", "w"))
	# for match in hist["matches"]:
	# 	dets = api.get_match_details(match["match_id"])
	# 	pprint(dets, indent = 2, stream = open("matches/%d" % match["match_id"], "w"))

if __name__ == "__main__":
	load_dotenv(find_dotenv())
	main(sys.argv[1:])
