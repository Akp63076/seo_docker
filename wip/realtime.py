from time import time

import httplib2
import requests
from oauth2client.service_account import ServiceAccountCredentials

GA_CREDS = "E:\\flask_project\\seoTool\\web_analytics\\auth\\rank_tool_api.json"
OAUTH_SCOPE = ["https://www.googleapis.com/auth/analytics.readonly"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(GA_CREDS, OAUTH_SCOPE)
print(credentials)

# Create requests session object (avoids need to pass in headers with every request)
session = requests.Session()
session.headers = {
    "Authorization": "Bearer " + credentials.get_access_token().access_token
}

# Enjoy!
url_kwargs = {
    "view_id": 86509496,  # Can be obtained from here: https://ga-dev-tools.appspot.com/account-explorer/
    "get_args": "metrics=rt:pageviews&dimensions=rt:pagePath",  # https://developers.google.com/analytics/devguides/reporting/realtime/v3/reference/data/realtime/get
}
response = session.get(
    "https://www.googleapis.com/analytics/v3/data/realtime?ids=ga:{view_id}&{get_args}".format(
        **url_kwargs
    )
)
response.raise_for_status()
result = response.json()
print(result)
