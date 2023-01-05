
import os  
sheetMap ={"blogs":{"alternate":"blogAlternateDay",
                   "monthly":"blogmonthly",
                           },
                   "collegedunia":{"bi_monthly_data":None,
                                   "monthly_data_1":None,
                                   "monthly_data_2":None,
                                   "monthly_data_3":None,
                                   "weekly_data_1":None,
                                   "weekly_data_2":None,
                                   "monthly_listing_kw":None,
                                    "quarterly":None,
                                    "daily_data":None,
                                   },
                   "prepp":{"bi_monthly_data":None,
                            "monthly_data":None,
                            "weekly_data":None,
                            },
                   "zoutons":{"uae":None,
                              "ksa": None},
                   "study_abroad":{"bi_monthly_data":None,
                                   "monthly_data":None,
                                   "weekly_data":None
                                   },
                   "left" :{"additional_1":None,
                            "additional" : None},
                    'log':None
                   }


def make_dirs_from_dict(d, current_dir):
    for key, val in d.items():
        os.mkdir(os.path.join(current_dir, key))
        if type(val) == dict:
             make_dirs_from_dict(val, os.path.join(current_dir, key))

os.mkdir('/home/ranking_data')     
dir_path=['/home/ranking_data/uploads','/home/ranking_data/uploaded']        
for dir_path in dir_path:
    os.mkdir(dir_path)
    make_dirs_from_dict(sheetMap,dir_path)