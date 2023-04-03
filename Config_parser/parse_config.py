import pandas_gbq
import psycopg2
import clickhouse_connect
from setuptools import setup, find_packages
import os.path
import configparser
import json
from google.oauth2 import service_account

setup(
    name='parse_config',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'configparser',
        'pandas',
        'matplotlib',
        'sklearn',
        'numpy',
        'seaborn'
    ],
    entry_points={
        'console_scripts': [
            'parse_config=parse_config:main'
        ]
    }
)

def connection_BQ(query, credentials):

    SCOPES = [
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/drive',
    ]
    df = pandas_gbq.read_gbq(query, project_id='loto-analytics', credentials=credentials)
    return df


def connection_CH(query, credentials):

    client = clickhouse_connect.get_client(credentials)
    client.command(query)
    df = client.query(query)
    return df


def connection_PSQL(query, credentials):

    # Подключение к существующей базе данных
    connection = psycopg2.connect(credentials)
    # Курсор для выполнения операций с базой данных
    cursor = connection.cursor()
    cursor.execute(query)
    df = cursor.fetchone()
    if connection:
        cursor.close()
        connection.close()
    return df


with open('credentials.json') as f:
    data = json.load(f)

DB = data['database_name']
print(DB)

query = """SELECT * 
FROM loto-analytics.belbet.client_events_production """

credentials = service_account.Credentials.from_service_account_file(
    '/Users/anast/PycharmProjects/Practice/credentials.json')

if DB == 'PostgreSQL':
    df = connection_PSQL(query, credentials)
elif DB == 'BigQuery':
    df = connection_BQ(query, credentials)
elif DB == 'ClickHouse':
    df = connection_CH(query, credentials)

#path = r'C:\Users\anast\PycharmProjects\Practice'
#config_folder = os.path.abspath(os.path.dirname('Practice'))

# полный путь к конфигурационному файлу
#config_file_path = os.path.join(path, config_file_name)

#config = configparser.ConfigParser()
#config.read(config_file_path)


# установка пакетов
import subprocess
required_packages = ['pandas', 'matplotlib', 'sklearn', 'numpy', 'seaborn']

for package in required_packages:
    try:
        import package
    except ImportError:
        subprocess.check_call(['pip', 'install', package])
