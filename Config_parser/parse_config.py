import pandas_gbq
import psycopg2
import clickhouse_connect
import os
# from setuptools import setup, find_packages
# import os.path
# import configparser
import json
from google.oauth2 import service_account


# setup(
#    name='parse_config',
#    version='1.0',
#    packages=find_packages(),
#    install_requires=[
#        'configparser',
#        'pandas',
#        'matplotlib',
#        'sklearn',
#        'numpy',
#        'seaborn'
#    ],
#    entry_points={
#        'console_scripts': [
#            'parse_config=parse_config:main'
#        ]
#    }
# )
class Connector:
    def connect_DBMS(self, DB, query, desktop_user, data):
        global df
        if DB == 'PostgreSQL':

            # Подключение к существующей базе данных
            connection = psycopg2.connect(database=data['database_name'],
                                          password=data['password'], user=data['user_name'])
            # Курсор для выполнения операций с базой данных
            cursor = connection.cursor()
            cursor.execute(query)
            df = cursor.fetchone()
            if connection:
                cursor.close()
                connection.close()

        elif DB == 'BigQuery':
            # SCOPES = [
            #    'https://www.googleapis.com/auth/cloud-platform',
            #    'https://www.googleapis.com/auth/drive',
            # ]
            credentials = service_account.Credentials.from_service_account_file(desktop_user)
            df = pandas_gbq.read_gbq(query, project_id='project_name', credentials=credentials)

        elif DB == 'ClickHouse':
            client = clickhouse_connect.get_client(database=data['database_name'],
                                          password=data['password'], user=data['user_name'])
            client.command(query)
            df = client.query(query)
        return df

query = """SELECT * 
FROM loto-analytics.belbet.client_events_production """

print(os.path.expanduser('~'))
desktop_user = os.path.expanduser("~\PycharmProjects\Practice\Config_parser\credentials.json")
print(desktop_user)


with open('credentials.json') as f:
    data = json.load(f)
DB = data['database_name']
print(data)
print(type(data))
print(DB)

connect = Connector()
df = connect.connect_DBMS(DB, query, desktop_user, data)


# установка пакетов
import subprocess
required_packages = ['pandas', 'matplotlib', 'sklearn', 'numpy', 'seaborn']

for package in required_packages:
    try:
        import package
    except ImportError:
        subprocess.check_call(['pip', 'install', package])
