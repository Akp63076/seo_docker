#!/bin/bash

source /home/django_app/myenv/bin/activate
cd /home/django_app/seo/
celery -A seoTool worker --loglevel=info 
