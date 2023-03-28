import configparser

config = configparser.ConfigParser()
config['credentials'] = {'URL': '*link*',
                     'username': 'hello_im_user',
                     'password': 'SECRET'}

with open('credentials.ini', 'w') as configfile: config.write(configfile)
