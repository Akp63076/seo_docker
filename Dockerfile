FROM python:3.8.6-slim-buster
ENV PYTHONUNBUFFERED 1
WORKDIR /seo-Tools
COPY .  .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt  --no-cache-dir 
RUN python manage.py makemigrations
RUN python manage.py migrate 
RUN python folder_creation.py
EXPOSE 8000 

CMD python manage.py runserver 0.0.0.0:8000