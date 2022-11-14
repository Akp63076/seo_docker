# seo

clone repo

install python : https://www.python.org/downloads/

for macos/linux
install pip : python3 -m pip install --user --upgrade pip
check version(make sure its latest ver) : python3 -m pip --version

instal virtualenv : python3 -m pip install --user virtualenv
create virtualen : python3 -m venv env

source env/bin/activate
pip install -r requirements.txt

to run project python manage.py runserver

#change required
change user name and password for database in setting .py and task.py
changing data path in ranktracker.celery.py line no. 28  (and in task.py for keyword data in special cases)
change allowed host in setting . py 


#change required for hosting
changing path in gunicorn service 
change path and domain in nginx configuration 
change  path in supervisor for celery
change celery shedule time in celery.py

