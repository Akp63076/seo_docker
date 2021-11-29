from django.shortcuts import render
from django.http import HttpResponse

import os
from glob import glob

data_folder = "static/ranking/data"
# static/ranking/data/2021-11-15/modified/combined_csv_modified.csv
#/Users/collegedunia/Documents/flask_project/seoTool/ranking/static/ranking/data/2021-11-15/result/Courses-result.csv

date_dir = glob(os.path.join(data_folder,"20*"))
result_dir = glob(os.path.join(data_folder,"20*","*","combined_csv_result.csv"))
modified_dir = glob(os.path.join(data_folder,"20*","*","combined_csv_modified.csv"))
print(result_dir)
print(modified_dir)

# Create your views here.
structure = []
for x,y,z in zip(date_dir,result_dir,modified_dir):
    structure.append({
        'date_dir':x.replace("static/ranking/data/",""),
        'result_dir':y,
        "modified_dir":z,
    })
print(structure)
structure.sort(key = lambda x:x['date_dir'],reverse=True)


def index(request):

    return render(request, 'ranking/index.html',{"context":structure})


# def wonwreport(request):

#     return HttpResponse "wow report will be shown here"