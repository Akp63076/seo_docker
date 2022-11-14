from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
#form
from .forms import Myform 
#celery
from redshiftClicks.tasks import sendRedshiftEmail
from celery.result import AsyncResult

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


@login_required
def index(request):
    form = Myform()
    return render(request, 'redshiftClicks/indexform.html', {'form':form})




#route("/start",methods=['POST'])
def longtask(request):
    if request.method == 'POST':#and  request.is_ajax:        
        # form = Myform(request.POST)
        print(request)
        logger.info(request)
        Link = request.POST['Link']
        email = request.POST['email']
        Range = request.POST['Range']
        request.session['url'] = Link
        request.session['duration'] = Range
        print(Link,email,Range)
        logger.info(Link,email,Range)
        
        task = sendRedshiftEmail.apply_async(args=[Link,email,Range])
        request.session['task_id'] =task.id        
        return JsonResponse({'task_id':task.id},status=202)


#route('status/<task_id>')
def taskstatus(request,task_id):
    try:
        task = AsyncResult(task_id)
        if task.state == 'PENDING':
            # job did not start yet
            response = {
                'state': task.state,
                'current': 0,
                'total': 1,
                'status': 'Loading...'
            }
        elif task.state != 'FAILURE':
            response = {
                'state': task.state,
                'current': task.get('current', 0),
                'total': task.get('total', 1),
                'status': task.get('status', '')
            }
            if 'result' in task.info:
                response['result'] = task.info['result']
        else:
            # something went wrong in the background job
            response = {
                'state': task.state,
                'current': 1,
                'total': 1,
                'status': str(task.info),  # this is the exception raised
            }
    except Exception as e:
        print(e)
        response = {
            'state' : 'ALMOST THERE',
            'current': 5,
            'total': 0,
            'status':"Almost There"
        }

    return JsonResponse(response)