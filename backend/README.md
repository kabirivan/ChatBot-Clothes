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

# SNNIPED FOR RESET PASSWORD
from django.contrib.auth import get_user_model
def reset_password(u, password):
    try:
        user = get_user_model().objects.get(email=u)
    except:
        return "User could not be found"
    user.set_password(password)
    user.save()
    return "Password has been changed successfully"