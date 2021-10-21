# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 17:43:38 2021

@author: collegedunia
"""

import pandas as pd

course_file = pd.read_excel('E:/flask_project/seoTool/coursefinder/static/coursefinder/csv/canada_mvp.xlsx',
                            sheet_name='course')



# course = course.applymap(lambda x: x.strip() if type(x) == str else x)
# course = course.applymap(lambda x: x.lower() if type(x) == str else x)

#create new id and name

# course_file['head_two'] = course_file[['head_two']].applymap(lambda x: x.strip() if type(x) == str else x)
uniquecourse = course_file['head_two'].dropna().unique()

index = [i for i in range(1000,uniquecourse.shape[0]+10000)]
coursedata = pd.DataFrame([[x,y] for x,y in zip(index,uniquecourse)],columns=['headID','head_two'])
# coursedata = coursedata.drop(0)

for i in range(course_file.shape[0]):
    stream = course_file.loc[i,"new_sub_streams"]
    course = course_file.loc[i,"head_two"]
    course_file.loc[i,'levelID'] = course_file.loc[i,'levelID']
    if stream == course:
        print(stream,course,1)
        course_file.loc[i,'Program_name'] = course_file.loc[i,'new_sub_streams']
        course_file.loc[i,'streamID'] = course_file.loc[i,'new_sub_streamsID']
    elif course =='-':
        course_file.loc[i,'Program_name'] = course_file.loc[i,'new_sub_streams']
        course_file.loc[i,'streamID'] = course_file.loc[i,'new_sub_streamsID']
    else :
        print(stream,course,0)
        course_file.loc[i,'streamID'] = coursedata.loc[list(coursedata['head_two']).index(course),'headID']
        course_file.loc[i,'Program_name'] = stream + "-" +course
        
course_file.drop_duplicates(inplace=True)
course_file.to_csv("E:/flask_project/seoTool/coursefinder/static/coursefinder/csv/course.csv")