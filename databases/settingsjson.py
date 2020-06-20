import json
import csv

csvDB = './databases/database.csv'

f = open(csvDB, 'r')
users = ['']

with f:
    reader = csv.DictReader(f)

    for row in reader:
        temp = row['name']+' ('+row['pin'][:-2]+')'
        users.append(temp)

settings_json = json.dumps([
    {'type': 'title',
     'title': 'Switches'},
    {'type': 'bool',
     'title': 'Party Mode',
     'desc': 'Removes some settings and config options',
     'section': 'settings',
     'key': 'partyMode'},
     {'type': 'bool',
      'title': 'Pin Mode',
      'desc': 'Requires a pin to pour a drink',
      'section': 'settings',
      'key': 'pinMode'},
     {'type': 'bool',
      'title': 'Dark Mode',
      'desc': 'Makes white the primary color and green the secondary',
      'section': 'settings',
      'key': 'darkMode'}
])

users_json = json.dumps([
    {'type': 'title',
     'title': 'Add a User'},
    {'type': 'string',
     'title': 'Enter Name',
     'desc': 'Type your name here',
     'section': 'users',
     'key': 'entername'},
     {'type': 'bool',
      'title': 'Enter Your Pin',
      'desc': 'Type in your pin number (can not be changed later as of now)',
      'section': 'users',
      'key': 'enterpin'},
     {'type': 'title',
      'title': 'Add Credits'},
    {'type': 'options',
     'title': 'Pick User',
     'desc': 'Pick the user from the list of users',
     'section': 'users',
     'key': 'userslist',
     'options': users},
     {'type': 'numeric',
      'title': 'Enter Credits Amount',
      'desc': 'Type in the amount of credits to add to the user',
      'section': 'users',
      'key': 'userscredits'
     }
])

# template_json = json.dumps([
#     {'type': 'title',
#      'title': 'Template'},
#     {'type': 'bool',
#      'title': 'A boolean setting',
#      'desc': 'Boolean description text',
#      'section': 'settings',
#      'key': 'partyMode'},
#     {'type': 'numeric',
#     'title': 'A numeric setting',
#     'desc': 'Numeric description text',
#     'section': 'settings',
#     'key': 'numericexample'},
#     {'type': 'options',
#     'title': 'An options setting',
#     'desc': 'Options description text',
#     'section': 'settings',
#     'key': 'optionsexample',
#     'options': ['option1', 'option2', 'option3']},
#     {'type': 'string',
#     'title': 'A string setting',
#     'desc': 'String description text',
#     'section': 'settings',
#     'key': 'stringexample'},
#     {'type': 'path',
#     'title': 'A path setting',
#     'desc': 'Path description text',
#     'section': 'settings',
#     'key': 'pathexample'}
# ])
