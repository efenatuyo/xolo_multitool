from src import multi
import json

multi(json.loads(open("config.json", "r").read())).choose_option()