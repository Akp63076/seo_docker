"""
resource : https://www.blueclaw.co.uk/2020/04/09/find-keyword-search-volumes-for-free-using-python-and-the-adwords-api/
https://developers.google.com/adwords/api/docs/guides/first-api-call#python_2
https://github.com/googleads/googleads-python-lib/tree/master/examples/adwords/authentication
"""

from zeep.xsd.types.complex import ComplexType
import _locale
import googleads
import pandas as pd
import traceback
from googleads import adwords
from googleads import oauth2

_locale._getdefaultlocale = (lambda *args: ['en_UK', 'UTF-8'])

class searchVolumePuller():
    def __init__(self,client_ID,client_secret,refresh_token,developer_token,client_customer_id):
        self.client_ID = client_ID
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.developer_token = developer_token
        self.client_customer_id = client_customer_id
            
    def get_client(self):
        access_token = oauth2.GoogleRefreshTokenClient(self.client_ID,
                                                        self.client_secret,
                                                        self.refresh_token)
        adwords_client = adwords.AdWordsClient(self.developer_token,
                                                access_token,
                                                client_customer_id = self.client_customer_id,
                                                cache=googleads.common.ZeepServiceProxy.NO_CACHE)

        return adwords_client
      
    def get_service(self,service,client):

        return client.GetService(service)

    def get_search_volume(self,service_client,keyword_list):
        #empty dataframe to append data into and keywords and search volume lists#
        keywords = []
        search_volume = []
        Competition =[]
        keywords_and_search_volume = pd.DataFrame()
        #need to split data into smaller lists of 700#
        sublists = [keyword_list[x:x+700] for x in range(0,len(keyword_list),700)]
        for sublist in sublists:
                # Construct selector and get keyword stats.
                selector = {
                'ideaType': 'KEYWORD',
                'requestType' : 'IDEAS'
                }
                
                #select attributes we want to retrieve#
                selector['requestedAttributeTypes'] = [
                'KEYWORD_TEXT',
                'SEARCH_VOLUME',
                'COMPETITION'
                ]
                
                #configure selectors paging limit to limit number of results#
                offset = 0
                selector['paging'] = {
                'startIndex' : str(offset),
                'numberResults' : 100
                    }
                
                #specify selectors keywords to suggest for#
                selector['searchParameters'] = [{
                'xsi_type' : 'RelatedToQuerySearchParameter',
                'queries' : sublist
                }
                    ]
                
                #pull the data#
                page = service_client.get(selector)
                #access json elements to return the suggestions#
                for i in range(0,len(page['entries'])):
                    keywords.append(page['entries'][i]['data'][0]['value']['value'])
                    search_volume.append(page['entries'][i]['data'][1]['value']['value'])
                    
        keywords_and_search_volume['Keywords'] = keywords
        keywords_and_search_volume['Search Volume'] = search_volume
        
        return keywords_and_search_volume

YOUR_CLIENT_ID = "734398090554-5v1blm5bi6a63qabn3qrum4m9cokrvms.apps.googleusercontent.com"
YOUR_CLIENT_SECRET = "bufs_CikgeY5kMxitZ1rPVpQ"
YOUR_REFRESH_TOKEN ="1//0gvqgaN4g3ooJCgYIARAAGBASNwF-L9IrwMEuhlVApaeL6cGoPeWGvvkpcsjJMZCracawzgkhDUMDiHTkI2qau0V1lT61deQWQok"
YOUR_DEVELOPER_TOKEN="Qz87gViNeH7byerGJ8L9fg"
YOUR_CLIENT_CUSTOMER_ID = "306-118-8621"

if __name__ == '__main__':
     CLIENT_ID = YOUR_CLIENT_ID
     CLIENT_SECRET = YOUR_CLIENT_SECRET
     REFRESH_TOKEN = YOUR_REFRESH_TOKEN
     DEVELOPER_TOKEN = YOUR_DEVELOPER_TOKEN
     CLIENT_CUSTOMER_ID = YOUR_CLIENT_CUSTOMER_ID

     keyword_list = ["jee main","neet"]

     volume_puller = searchVolumePuller(CLIENT_ID,
                                        CLIENT_SECRET,
                                        REFRESH_TOKEN,
                                        DEVELOPER_TOKEN,
                                        CLIENT_CUSTOMER_ID)

     adwords_client = volume_puller.get_client()
            
            
     targeting_service = volume_puller.get_service('TargetingIdeaService', adwords_client)

     kw_sv_df = volume_puller.get_search_volume(targeting_service,keyword_list)

     print(kw_sv_df)