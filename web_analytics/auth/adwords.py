"""
resource : https://www.blueclaw.co.uk/2020/04/09/find-keyword-search-volumes-for-free-using-python-and-the-adwords-api/
https://developers.google.com/adwords/api/docs/guides/first-api-call#python_2
https://github.com/googleads/googleads-python-lib/tree/master/examples/adwords/authentication
https://developers.google.com/adwords/api/docs/reference/v201809/TargetingIdeaService.TargetingIdeaSelector

"""

import _locale
import googleads
import pandas as pd
import traceback
from googleads import adwords
from googleads import oauth2

_locale._getdefaultlocale = (lambda *args: ['en_UK', 'UTF-8'])
PAGE_SIZE = 700

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

      def get_search_volume(self,service_client,keyword_list ,count,requesttype='STATS'):
            #empty dataframe to append data into and keywords and search volume lists#
            keywords = []
            search_volume = []
            competition = []
            keywords_and_search_volume = pd.DataFrame()
            
            
            
            # Construct selector and get keyword stats/ideas.
            selector = {
            'ideaType': 'KEYWORD',
            'requestType' : requesttype
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
            'numberResults' : str(PAGE_SIZE)
                  }
                    
            #specify selectors keywords to suggest for#
            selector['searchParameters'] = [{
            'xsi_type' : 'RelatedToQuerySearchParameter',
            'queries' : keyword_list
                  },
                  
                  {
              # Location setting (optional).
              # The ID can be found in the documenation:
              #  https://developers.google.com/adwords/api/docs/appendix/geotargeting
              # Country codes found by searching country name in name filter
              'xsi_type': 'LocationSearchParameter',
              'locations': [{'id': 2356}]
          },
          {
              # Network search parameter (optional)
              'xsi_type': 'NetworkSearchParameter',
              'networkSetting': {
                  'targetGoogleSearch': True,
                  'targetSearchNetwork': False,
                  'targetContentNetwork': False,
                  'targetPartnerSearchNetwork': False

              }
          }]
                
            #pull the data#
            page = service_client.get(selector)
            print(len(page['entries']))
            # print(page)
            if 'entries' in page:
            #access json elements to return the suggestions#
                  for i in range(0,len(page['entries'])):
                        keywords.append(page['entries'][i]['data'][0]['value']['value'])
                        search_volume.append(page['entries'][i]['data'][2]['value']['value'])
                        competition.append(page['entries'][i]['data'][1]['value']['value'])
            else :
                  print('No keywords were found.')
          

                              
            keywords_and_search_volume['keywords'] = keywords
            keywords_and_search_volume['search_volume'] = search_volume
            keywords_and_search_volume['competition'] = competition
            
            return keywords_and_search_volume
        
YOUR_CLIENT_ID = "734398090554-5v1blm5bi6a63qabn3qrum4m9cokrvms.apps.googleusercontent.com"
YOUR_CLIENT_SECRET = "bufs_CikgeY5kMxitZ1rPVpQ"
YOUR_REFRESH_TOKEN ="1//0gvqgaN4g3ooJCgYIARAAGBASNwF-L9IrwMEuhlVApaeL6cGoPeWGvvkpcsjJMZCracawzgkhDUMDiHTkI2qau0V1lT61deQWQok"
YOUR_DEVELOPER_TOKEN="Qz87gViNeH7byerGJ8L9fg"
YOUR_CLIENT_CUSTOMER_ID = "306-118-8621"

CLIENT_ID = YOUR_CLIENT_ID
CLIENT_SECRET = YOUR_CLIENT_SECRET
REFRESH_TOKEN = YOUR_REFRESH_TOKEN
DEVELOPER_TOKEN = YOUR_DEVELOPER_TOKEN
CLIENT_CUSTOMER_ID = YOUR_CLIENT_CUSTOMER_ID

# keyword_list = ['SEO','Leeds','Google']

volume_puller = searchVolumePuller(CLIENT_ID,
                                    CLIENT_SECRET,
                                    REFRESH_TOKEN,
                                    DEVELOPER_TOKEN,
                                    CLIENT_CUSTOMER_ID)

adwords_client = volume_puller.get_client()
            
            
targeting_service = volume_puller.get_service('TargetingIdeaService', adwords_client)

def kwvolume(keyword_list = ['SEO','Leeds','Google']):
      count = str(len(keyword_list))

      try : 
            kw_sv_df = volume_puller.get_search_volume(targeting_service,keyword_list,count,"STATS")
      # print(kw_sv_df)
      except:
            kw_sv_df = pd.DataFrame(columns =['keywords','search_volume','competition'])
      return kw_sv_df

def kwIdeas(keyword_list = ['SEO','Leeds','Google']):

      count=PAGE_SIZE
      try :
            kw_sv_df = volume_puller.get_search_volume(targeting_service,keyword_list,count,"IDEAS")
      # print(kw_sv_df)
      except: 
            kw_sv_df = pd.DataFrame(columns =['keywords','search_volume','competition'])
      return kw_sv_df

     