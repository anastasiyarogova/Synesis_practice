import json

with open('credentials.json', 'w') as f:
    print("The json file is created")

config = {'database_name': 'PostgreSQL',
          'user_name': 'hello_im_user',
          'password': 'SECRET',
          'client_email': '***'}


with open('credentials.json', 'w') as f:
    json.dump(config, f,  sort_keys=True, indent=2)

with open('credentials.json') as f:
    print(f.read())


