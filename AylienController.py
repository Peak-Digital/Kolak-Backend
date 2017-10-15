import aylien_news_api
import json
import random
from aylien_news_api.rest import ApiException

search_topics = ["trump", "gun control", "abortion", "LGBT", "immigration",
               "taxes", "politics", "religion", "hillary", "ACLU", 
               "climate change", "global warming", "death penalty",
               "gay marriage", "minimum wage", "democrats", "republicans",
               "border", "oil", "foreign aid", "prison", "drugs", "Terrorism"]

proper_sources = ['The New York Times', 'Wall Street Journal', 'BBC', 
                  'The New Yorker' , 'Politico', 'Oxford University Press',
                  'Washington Examiner', 'Boston Herald', 'The Guardian',
                  'The Washington Post', 'The Hill', 
                  'Newsweek', 'Business Insider', 'Cornell Daily Sun'
                 ]

ban_sources = ['The Onion', 'Liverpool Echo', 'Associated Press', 
               'The Star - Toronto', 'Daily Mail UK' , 'Daily Mail'
        ]

class AylienAccessor:

    def __init__(self):
        # Configure API key authorization: app_id
        aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = 'a172ccb3'
        # Configure API key authorization: app_key
        aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = '94ae210372549948dd15ed3dc3f5c0dd'
        
        self.api_instance = None

        # create an instance of the API class
        self.api_instance = aylien_news_api.DefaultApi()

    def getStories(self, search_query, title_polarity = "neutral", body_polarity= "neutral", per_page = 5):

        search = { #Generic search query, primarily focused on topic and sentiment polarity
            'title': search_query,
            'sort_by': 'social_shares_count.facebook',
            'language': ['en'],
            'published_at_start': 'NOW-7DAYS',
            'published_at_end': 'NOW',
            'per_page': per_page,
            'categories_confident': 'false',
            'source_locations_country': ['US'],
            'source_name': proper_sources,
            'not_sentiment_title_polarity': "negative",
            'not_sentiment_body_polarity': "negative"
        }

        try:
            # List stories
            api_response = self.api_instance.list_stories(**search) #Get results from API
            return api_response

        except ApiException as e:
            print("Exception when calling DefaultApi->list_stories: %s\n" % e)

    #Get a bait story. Bait = negative polarity for both title and body
    def getBaitStories(self, search_query, title_polarity = "negative", body_polarity = "negative", per_page = 10):

        search = { #Generic search query, primarily focused on topic and sentiment polarity
            'title': search_query,
            'sort_by': 'social_shares_count.facebook',
            'language': ['en'],
            'published_at_start': 'NOW-30DAYS',
            'published_at_end': 'NOW',
            'not_source_name': ban_sources,
            'per_page': per_page,
            'source_locations_country': ['US'],
            'not_source_name': ban_sources,
            'sentiment_title_polarity': title_polarity,
            'sentiment_body_polarity': body_polarity
        }

        try:
            # List stories
            api_response = self.api_instance.list_stories(**search) #Get results from API
            return api_response

        except ApiException as e:
            print("Exception when calling DefaultApi->list_stories: %s\n" % e)

    def getRandBait(self):
        return self.getBaitStories(search_topics[random.randint(0, len(search_topics) - 1)])    #Get random bait

    def getMixedResults(self):
        random.seed()
        retVal = []
        for i in range(0, 5):
            storiesObj = self.getRandBait().stories
            for storyObj in storiesObj:

                response = {    #Assemble relevant bits in to collection for cards
                    'title': storyObj.title,
                    'source': storyObj.source.name,
                    'url': storyObj.links.permalink,
                    'bait': 'true'
                }

                retStr = ""
                for stri in storyObj.summary.sentences:
                    retStr += stri

                response['summary'] = retStr

                response['reduced'] = (100 - (((float)(len(retStr.split())) / len(storyObj.body)) * 100))

                for content in storyObj.media:  #get first image from media
                    if content.type == "image" and "logo" not in content.url:
                        response["image"] = content.url
                        print "Accepted url: " + content.url
                        break   #we found an image to use
                    else:
                        print "Rejected Image: " + content.url

                retVal.append(response) #This happens five times, due to requested number of elements

        for i in range(0, 3):
            storiesObj = self.getStories(search_topics[random.randint(0, len(search_topics) - 1)]).stories
            for storyObj in storiesObj:

                response = {    #Assemble relevant bits in to collection for cards
                    'title': storyObj.title,
                    'source': storyObj.source.name,
                    'url': storyObj.links.permalink,
                    'bait': 'false'
                }

                retStr = ""
                for stri in storyObj.summary.sentences:
                    retStr += stri

                response['summary'] = retStr

                response['reduced'] = (100 - (((float)(len(retStr.split())) // len(storyObj.body)) * 100))

                for content in storyObj.media:  #get first image from media
                    if content.type == "image" and "logo" not in content.url:
                        response["image"] = content.url
                        print "Accepted url: " + content.url
                        break   #we found an image to use
                    else:
                        print "Rejected Image: " + content.url

                retVal.append(response) #This happens five times, due to requested number of elements
        random.shuffle(retVal)
        print "Returned " + str(len(retVal)) + " articles\n"
        return retVal