#!/usr/bin/env python
# python google_ad_api.py -c 3061188621 -l 20456 -i 1000 -k neet
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This example generates keyword ideas from a list of seed keywords."""
 
 
import argparse
import sys
import time
from time import sleep

import pandas as pd
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Location IDs are listed here:
# https://developers.google.com/google-ads/api/reference/data/geotargets
# and they can also be retrieved using the GeoTargetConstantService as shown
# here: https://developers.google.com/google-ads/api/docs/targeting/location-targeting
_DEFAULT_LOCATION_IDS = ["2356"]  # location ID for new delhi
# A language criterion ID. For example, specify 1000 for English. For more
# information on determining this value, see the below link:
# https://developers.google.com/google-ads/api/reference/data/codes-formats#expandable-7
_DEFAULT_LANGUAGE_ID = "1000"  # language ID for English
 
 
# [START generate_keyword_ideas]
def main(
    client, customer_id, location_ids, language_id, keyword_texts, page_url
):
    keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")
    keyword_competition_level_enum = client.get_type(
        "KeywordPlanCompetitionLevelEnum"
    ).KeywordPlanCompetitionLevel
    keyword_plan_network = client.get_type(
        "KeywordPlanNetworkEnum"
    ).KeywordPlanNetwork.GOOGLE_SEARCH_AND_PARTNERS
    location_rns = _map_locations_ids_to_resource_names(client, location_ids)
    language_rn = client.get_service("GoogleAdsService").language_constant_path(
        language_id
    )
     
    keyword_annotation = client.enums.KeywordPlanKeywordAnnotationEnum
     
    # Either keywords or a page_url are required to generate keyword ideas
    # so this raises an error if neither are provided.
    if not (keyword_texts or page_url):
        raise ValueError(
            "At least one of keywords or page URL is required, "
            "but neither was specified."
        )
     
     
     
    # Only one of the fields "url_seed", "keyword_seed", or
    # "keyword_and_url_seed" can be set on the request, depending on whether
    # keywords, a page_url or both were passed to this function.
    request = client.get_type("GenerateKeywordIdeasRequest")
    request.customer_id = customer_id
    request.language = language_rn
    request.geo_target_constants = location_rns
    request.include_adult_keywords = False
    request.keyword_plan_network = keyword_plan_network
    request.keyword_annotation = keyword_annotation
     
     
     
    # To generate keyword ideas with only a page_url and no keywords we need
    # to initialize a UrlSeed object with the page_url as the "url" field.
    if not keyword_texts and page_url:
        request.url_seed.url = url_seed
 
    # To generate keyword ideas with only a list of keywords and no page_url
    # we need to initialize a KeywordSeed object and set the "keywords" field
    # to be a list of StringValue objects.
    if keyword_texts and not page_url:
        request.keyword_seed.keywords.extend(keyword_texts)
 
    # To generate keyword ideas using both a list of keywords and a page_url we
    # need to initialize a KeywordAndUrlSeed object, setting both the "url" and
    # "keywords" fields.
    if keyword_texts and page_url:
        request.keyword_and_url_seed.url = page_url
        request.keyword_and_url_seed.keywords.extend(keyword_texts)
 
    keyword_ideas = keyword_plan_idea_service.generate_keyword_ideas(
        request=request
    )
     
    list_keywords = []
    for idea in keyword_ideas:
        competition_value = idea.keyword_idea_metrics.competition
        list_keywords.append(idea)
     
    return list_keywords
 
def map_keywords_to_string_values(client, keyword_texts):
    keyword_protos = []
    for keyword in keyword_texts:
        string_val = client.get_type("StringValue")
        string_val.value = keyword
        keyword_protos.append(string_val)
    return keyword_protos
 
 
def _map_locations_ids_to_resource_names(client, location_ids):
    """Converts a list of location IDs to resource names.
    Args:
        client: an initialized GoogleAdsClient instance.
        location_ids: a list of location ID strings.
    Returns:
        a list of resource name strings using the given location IDs.
    """
    build_resource_name = client.get_service(
        "GeoTargetConstantService"
    ).geo_target_constant_path
    return [build_resource_name(location_id) for location_id in location_ids]
 
 
def bulkKeywordPlanner(keywords):
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage("web_analytics/auth/google-ads.yaml")  
 
    try:
            list_keywords =  main(
                    googleads_client,
                "3061188621", ["2356"], "1000", keywords, None
                )
    
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
    # for i in range(1,len(list_keywords)+1):
    #             #  print(list_keywords)
    #           print(i)
    list_to_excel = []
    for x in range(len(list_keywords)):
        list_months = []
        list_searches = []
        list_annotations = []
        for y in list_keywords[x].keyword_idea_metrics.monthly_search_volumes:
            list_months.append(str(y.month)[12::] + " - " + str(y.year)) 
            list_searches.append(y.monthly_searches)
            
        for y in list_keywords[x].keyword_annotations.concepts:
            list_annotations.append(y.concept_group.name)
            
            
        list_to_excel.append([list_keywords[x].text, list_keywords[x].keyword_idea_metrics.avg_monthly_searches, str(list_keywords[x].keyword_idea_metrics.competition)[28::], list_keywords[x].keyword_idea_metrics.competition_index, ])

        # list_searches, list_months, list_annotations
    #     final_list = []
    #     for x in list_to_excel:
    #         final_list.append(x) 
    #         return final_list
    #     list1 = final_list
    # list1.append(final_list)
        bulkidea_df=pd.DataFrame(list_to_excel, columns = ["Keyword", "Average_Searches", "Competition_Level", "Competition_Index",])
        bulkidea_df['Regarding'] = pd.Series([keywords[0] for x in range(len(bulkidea_df.index))])
    
    return bulkidea_df    
        
# bulkKeywordPlanner(['neet','jee'])

def loopplanner(keywords):
    new_list=[] 
    df=pd.DataFrame()
    for i in keywords:
        new_list.append([i])
    print(new_list)
    count = 0 
    frames =[]
    for i in new_list:
        if count == new_list.index(i):
            globals()['df'+ str(count)] = bulkKeywordPlanner(i)
            frames.append(globals()['df'+ str(count)])
        count +=1
    if count == 1:
        result = df0
        result = result[result.Keyword.isin(keywords) == False]
        print(result)
        return result
    if count > 1:
        result = pd.concat(frames)
        # shape = result.shape
        # print("shape = {}".format(shape))
        # print(result)
        result = result[result.Keyword.isin(keywords) == False]
        return result

# loopplanner()


# for i in range(1,len(list_keywords)+1):

# #  print(list_keywords)
#  print(i)
# list_keywords = main(client, "306-118-8621", ["2840"], "1000", ["mortgage"], None)
# list_to_excel = []
# for x in range(len(list_keywords)):
#     list_months = []
#     list_searches = []
#     list_annotations = []
#     for y in list_keywords[x].keyword_idea_metrics.monthly_search_volumes:
#         list_months.append(str(y.month)[12::] + " - " + str(y.year))
#         list_searches.append(y.monthly_searches)
         
#     for y in list_keywords[x].keyword_annotations.concepts:
#         list_annotations.append(y.concept_group.name)
         
         
#     list_to_excel.append([list_keywords[x].text, list_keywords[x].keyword_idea_metrics.avg_monthly_searches, str(list_keywords[x].keyword_idea_metrics.competition)[28::], list_keywords[x].keyword_idea_metrics.competition_index, ])

    # list_searches, list_months, list_annotations 

 
    # pd.DataFrame(list_to_excel, columns = ["Keyword", "Average Searches", "Competition Level", "Competition Index", ]).to_excel('outputyearly.xlsx', header=True, index=False)
   
    # "Searches Past Months", "Past Months", "List Annotations"