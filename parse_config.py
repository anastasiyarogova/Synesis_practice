from setuptools import setup, find_packages
import os.path
import configparser

setup(
    name='my_module',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'configparser',
        'pandas',
        'matplotlib'
    ],
    entry_points={
        'console_scripts': [
            'my_module=my_module:main'
        ]
    }
)

config_file_name = "credentials.ini"

#path = r'C:\Users\anast\PycharmProjects\Practice'

config_folder = os.path.abspath(os.path.dirname('Practice'))

# полный путь к конфигурационному файлу
config_file_path = os.path.join(config_folder, config_file_name)

config = configparser.ConfigParser()
config.read(config_file_path)

username = config.get('credentials', 'username')
password = config.get('credentials', 'password')


# установка пакетов
import subprocess

# список необходимых пакетов
required_packages = ['pandas', 'matplotlib', 'sklearn', 'numpy', 'seaborn']

# проверяем, установлены ли требуемые пакеты
for package in required_packages:
    try:
        import package
    except ImportError:
        subprocess.check_call(['pip', 'install', package])