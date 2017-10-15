import aylien_news_api
import json
from aylien_news_api.rest import ApiException

# Configure API key authorization: app_id
aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = '843ed6b7'
# Configure API key authorization: app_key
aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = '5c1929a0d1e02bb5b4b4934bc3efb372'

# create an instance of the API class
api_instance = aylien_news_api.DefaultApi()

search_query = "trump"
polarity = "negative"

search = {
  'title': search_query,
  'sort_by': 'social_shares_count.facebook',
  'language': ['en'],
  'not_language': ['es', 'it'],
  'published_at_start': 'NOW-7DAYS',
  'published_at_end': 'NOW',
  'sentiment_title_polarity': polarity
}

try:
    # List stories
    api_response = api_instance.list_stories(**search)
    print("===========NEGATIVE===========")
    #print(api_response.stories)
    for story in api_response.stories:
      print(story.title)

    search["sentiment_title_polarity"] = "neutral"
    api_response = api_instance.list_stories(**search)
    print("\n===========NEUTRAL===========")
    for story in api_response.stories:
        print(story.title)

    search["sentiment_title_polarity"] = "positive"
    api_response = api_instance.list_stories(**search)
    print("\n===========POSITIVE===========")
    for story in api_response.stories:
        print(story.title)

except ApiException as e:
    print("Exception when calling DefaultApi->list_stories: %s\n" % e)