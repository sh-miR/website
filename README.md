# shmir-website #
[![GNU License](http://img.shields.io/badge/license-GNU-blue.svg)](http://www.gnu.org/licenses/gpl.html)
[![Documentation Status](https://readthedocs.org/projects/shmir-designer/badge/?version=latest)](http://shmir-designer.readthedocs.org/en/latest/)

Web client for [sh-miR Designer RESTful API](https://github.com/igemsoftware/AMU-Poznan2014/tree/master/shmir-api) written in Django.

How to run it in 4 simple steps:

1. Install requirements:
```
pip install -r requirements.txt
```
2. Synchronize database to create all needed tables and follow the instructions:
```
python manage.py syncdb
```
3. Set SHMIR_API_ADDRESS variable in shweb/shweb/settings.py file to proper sh-miR API url (official or local)
4. Type runserver command:
```
python manage.py runserver
```
Your local web-based client is ready for use on **127.0.0.1:8000**
