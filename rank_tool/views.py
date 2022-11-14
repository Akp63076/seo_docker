from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.conf import settings
from rank_tool.tasks import send_feedback_email_task
from rank_tool.forms import EmailModelForm
from django.contrib.auth.models import User
from rank_tool.models import upload
import pandas as pd
import datetime
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
    template = "rank_tool/index.html"
    if request.method == 'POST':
        form = EmailModelForm(request.POST, request.FILES)
        if form.is_valid():
            recipient_email = request.POST.get('email')
            file_name=request.FILES['file'].name
            newfile=upload(file = request.FILES['file'],email=recipient_email,file_name=request.FILES['file'].name,user=request.user,time_created=datetime.datetime.now())
            newfile.save()
            print(recipient_email)
            file_path=newfile.file_name
            print(newfile.id)
            send_feedback_email_task.delay(newfile.id)
            return redirect('rank_tool-queue')
    else:   
        form = EmailModelForm()
    return render(request, template, {'form': form,'user':request.user.first_name,'email':request.user.email})

@login_required
def queue(request):
    context={'queues': upload.objects.order_by('-time_created').all() }
    return render(request,"rank_tool/queue.html",context)

@login_required
def instructions(request):
    return render(request,"rank_tool/instructions.html")



