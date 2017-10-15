import msgraph

graph_base_url = 'https://graph.microsoft.com/v1.0/'
http_provider = msgraph.HttpProvider()
auth_provider = 

client = msgraph.GraphServiceClient(graph_base_url, http_provider, auth_provider)