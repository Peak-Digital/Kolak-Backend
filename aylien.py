import aylien_news_api
import json
import random
from aylien_news_api.rest import ApiException

bait_topics = ["trump", "gun control", "abortion", "LGBT", "immigration",
               "taxes", "politics", "religion", "hillary", "ACLU", 
               "climate change", "global warming", "death penalty",
               "gay marriage", "minimum wage", "democrats", "republicans",
               "border", "oil", "foreign aid", "prison"]

def getBaitStories(search_query, title_polarity = "negative", body_polarity = "negative"):
    return getStories(search_query, title_polarity)

def getRandBait():
    return getBaitStories(bait_topics[random.randint(0, len(bait_topics))])

def getStories(search_query, title_polarity, body_polarity= "neutral", per_page = 10):

    search = {
    'title': search_query,
    'sort_by': 'social_shares_count.facebook',
    'language': ['en'],
    'published_at_start': 'NOW-30DAYS',
    'published_at_end': 'NOW',
    'per_page': per_page,
    'sentiment_title_polarity': title_polarity,
    'sentiment_body_polarity': body_polarity
    }

    try:
        # List stories
        api_response = api_instance.list_stories(**search)
        return api_response

    except ApiException as e:
        print("Exception when calling DefaultApi->list_stories: %s\n" % e)

def formattedStory(search_query, title_polarity, body_polarity= "neutral", per_page = 10):
    pass

# Configure API key authorization: app_id
aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = '843ed6b7'
# Configure API key authorization: app_key
aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = '5c1929a0d1e02bb5b4b4934bc3efb372'

# create an instance of the API class
api_instance = aylien_news_api.DefaultApi()

result = getRandBait()
for res in result.stories:
    print(res.source.title)
    print(res.title)
    print("\n")