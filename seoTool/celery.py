from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seoTool.settings')
app = Celery('seoTool')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# Celery Beat Settings
app.conf.beat_schedule = {
    'update-database-at-every-monday': {
        'task': 'cd_ranking.tasks.database_update',
        'schedule':crontab(hour=5,minute=55),
       'args':["/home/ranking_data/uploads","/home/ranking_data/uploaded"]
            
                                        },
}







@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))