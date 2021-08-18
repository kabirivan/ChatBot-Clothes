## Create environment
python3 -m venv env
source env/bin/activate


## CREATE PROJECT
django-admin startproject chatbot .

## RUN PROJECT
python manage.py runserver


## REALIZAR MIGRACIONES MODELO
python manage.py makemigrations 
python manage.py migrate   

# CREATE SUPER USER
python manage.py createsuperuser