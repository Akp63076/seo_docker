from django.shortcuts import render
from django.http import HttpResponse
from .forms import Myform

#E:\flask_project\seoTool\redshiftClicks\templates
# Create your views here.
def index(request):
    
    if request.method == 'POST':
        form = Myform(request.POST)
        if form.is_valid():
            #input parameters 
            url = request.POST['Link']
            context = {}
            return render(request,'cd-status/result.html',context)
        else:
            form = Myform()
        
    return render(request, 'cd-status/indexform.html', {'form':form})
 