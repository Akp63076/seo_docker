import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

def updateDir(folder,sub_folder,output_timestamp,path):
    '''
    this fuction is made to update the file present in respect dir
    reference : https://docs.gspread.org/en/latest/
    '''
    sheetMap ={"blogs":{"alternate":"blogAlternateDay",
                   "monthly":"blogmonthly",
                           },
                   "collegedunia":{"bi_monthly_data":"bimonthly",
                                   "monthly_data_1":"monthly-1",
                                   "monthly_data_2":"monthly-2",
                                   "monthly_data_3":"monthly-3",
                                   "weekly_data_1":"weekly_1",
                                   "weekly_data_2":"weekly_2",
                                   "monthly_listing_kw":"kw-listing",
                                    "quarterly":"cd-quarterly",
                                    "daily_data":'daily',
                                   },
                   "prepp":{"bi_monthly_data":"prepp-bi",
                            "monthly_data":"prepp-monthly",
                            "weekly_data":"prepp-weekly",
                            },
                   "zoutons":{"uae":"zoutons",
                              "ksa": "zoutons"},
                   "study_abroad":{"bi_monthly_data":"sa-bi",
                                   "monthly_data":"sa-monthly",
                                   "weekly_data":"sa-weekly"
                                   },
                   "left" :{"additional_1":"testing",
                            "additional" : "temp"},
                   }
    
    gsheetFile = sheetMap[folder][sub_folder]
    
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    credentials = Credentials.from_service_account_file(
        "/home/seo/scrapers/auth/client_secret.json",
        scopes=scopes
    )

    gc = gspread.authorize(credentials)
    
    sh = gc.open("Ranking Schedule")
    
    #get all worksheets
    #worksheet_list = sh.worksheets()
    #print(worksheet_list)
    #print(sh.sheet1.get('A1'))
    
    #by num
    #worksheet = sh.get_worksheet(0)
    #by title
    worksheet = sh.worksheet(gsheetFile)
    print( "This is ", worksheet)
    values_list = worksheet.get_all_values()
    df = pd.DataFrame(values_list[1:],columns =values_list[0])
    df.to_csv(path,index=False)