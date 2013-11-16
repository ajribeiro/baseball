import json

request = json.load(sys.stdin)
response = {'resp':'in python, name='+request['name']}
json.dump(response, sys.stdout, indent=4)