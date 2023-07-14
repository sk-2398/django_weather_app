# django_weather_app
## Description
This repository helps you to create fullstack weather application using django restAPI. 
In this app we created API to fetch weather data from API provided by <a href="https://openweathermap.org/api/one-call-api">Open weather map organisation</a>.
And showing weather details based of location based on lattitude and longitude given as input.

## Instruction to run project on local

1) Clone this repository
2) Open terminal in root repository create virtual env and activate it
```bsh
virtualenv venv
venv/Scripts/activate
```
3) Install all packages given in requirements.txt file
```bsh
pip install -r requirements.txt
```
4) Run migration directly to create table in default database or add your custom database credential in setting.py
   To run migrations
```bsh
python manage.py makemigrations
python manage.py migrate
```
5) Get your API key from  <a href="https://openweathermap.org/api/one-call-api">Open weather map organisation</a>.
   and add it in views.py file of weather_app
   ![image](https://github.com/sk-2398/django_weather_app/assets/81793485/b80e4ca8-2c8f-47d2-98ec-14f3bdc2b758)
6) Run
```bsh
python manage.py runserver
```
to run this project. It will open project on http://127.0.0.1:8000/
