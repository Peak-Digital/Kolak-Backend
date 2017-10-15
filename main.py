import falcon
from AylienController import AylienAccessor
import json

class UnifiedList:

    def on_get(self, req, resp):
        print "Getting mixed results"
        f = AylienAccessor()

        ret_stories = f.getMixedResults()
        resp.body = json.dumps(ret_stories)

#Bait articles have a negative title and body
class BaitArticle:

    #GET HTTP responder
    def on_get(self, req, resp):
        print "Getting bait"
        f = AylienAccessor()

        ret_stories = f.getRandBait()   #get random bait
        retVal = []
        for storyObj in ret_stories.stories:

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

            for content in storyObj.media:  #get first image from media
                if content.type == "image" and "logo" not in content.url:
                    response["image"] = content.url
                    print "Accepted url: " + content.url
                    break   #we found an image to use
                else:
                    print "Rejected Image: " + content.url

            retVal.append(response) #This happens five times, due to requested number of elements
        print "Returned articles: " + str(len(retVal))
        resp.body = json.dumps(retVal)

    #POST HTTP handler
    def on_post(self, req, resp):

        requested_topic = json.loads(req.stream.read().decode('utf-8')) #Get request from POST
        print requested_topic   
        f = AylienAccessor()

        print("Getting bait stories for topic: " + requested_topic['topic'])
        ret_stories = f.getBaitStories(requested_topic['topic'])    #Get bait stories of specified topic
        retVal = []

        for storyObj in ret_stories.stories:
            response = {    #Information for card
                'title': storyObj.title,
                'source': storyObj.source.name,
                'url': storyObj.links.permalink,
                'bait': 'true'
                #'date': storyObj.published_at
            }
            
            retStr = ""
            for stri in storyObj.summary.sentences:
                retStr += stri

            response['summary'] = retStr

            for content in storyObj.media:
                if content.type == "image" and "logo" not in content.url: #try to find image for card
                    response["image"] = content.url
                    print "Accepted url: " + content.url
                    break   #found an image to use
                else:
                    print "Rejected Image: " + content.url

            retVal.append(response) #Five will be generated, specified in AylienController.py
        print "Returned articles: " + str(len(retVal))
        resp.body = json.dumps(retVal)

class NewsArticle:

    #GET HTTP handler
    def on_get(self, req, resp):
        f = AylienAccessor()

        storyObj = f.getStories("trump", "neutral") #This is just a basic query that's relevant
        print storyObj.stories[0].published_at
        response = {    #Assemble relevant information for cards
            'title': storyObj.stories[0].title,
            'source': storyObj.stories[0].source.name,
            'url': storyObj.stories[0].links.permalink,
            'bait': 'false'
        }

        retStr = ""
        for stri in storyObj.stories[0].summary.sentences:
            retStr += stri

        response['summary'] = retStr

        #print "Size reduce by: " + str(100 - (((float)(len(retStr.split())) / len(storyObj.stories[0].body)) * 100) ) + "%"

        for content in storyObj.stories[0].media:    #To to find image
                if content.type == "image":
                    response["image"] = content.url
                    print "Accepted url: " + content.url
                    break   #Found image
                else:
                    print "Rejected Image: " + content.url
        print "Returned articles: 1"
        resp.body = json.dumps(response)    #Hand out relevent card data

    #POST HTTP handler
    def on_post(self, req, resp):
        requested_topic = json.loads(req.stream.read().decode('utf-8'))
        f = AylienAccessor()

        print("Getting news stories for topic: " + requested_topic['topic'])
        ret_stories = f.getStories(requested_topic['topic'])    #Get news related to search query, specified 'topic' in JSON
        retVal = []

        for storyObj in ret_stories.stories:

            response = {    #Assemble card data
                'title': storyObj.title,
                'source': storyObj.source.name,
                'url': storyObj.links.permalink,
                'bait': 'false'
            }

            retStr = ""
            for stri in storyObj.summary.sentences:
                retStr += stri

            response['summary'] = retStr

            for content in storyObj.media:  #try to find image for card
                if content.type == "image" and "logo" not in content.url:
                    response["image"] = content.url
                    print "Accepted url: " + content.url
                    break   #Found image
                else:
                    print "Rejected Image: " + content.url

            retVal.append(response) #5 present, see AylienController.py
        print "Returned articles: " + str(len(retVal))
        resp.body = json.dumps(retVal)

api = falcon.API()  #The magic happens here
api.add_route('/api/bait', BaitArticle())   #Connect bait articles to /api/bait
api.add_route('/api/news', NewsArticle())   #Connect news articles to /api/news
api.add_route('/api/unified', UnifiedList())