import json
import requests
import os
import shutil

#Enter details...
OSF_TOKEN = '***'
USER_ID = '***'
loc = '***'

OSF_API_URL = 'https://api.osf.io/v2/'

#Function to print out responses
def pretty_print(json_data):
    print(json.dumps(json_data, indent=4))
    
#Define helper function
def post_request(url, data):
    headers = {
        'Content-Type': 'application/vnd.api+json',
        'Authorization': 'Bearer {}'.format(OSF_TOKEN)
    }
    data = json.dumps(data)
    return requests.post(url, headers=headers, data=data)

def get_request(url):
    headers = {'Authorization': 'Bearer {}'.format(OSF_TOKEN)}
    return requests.get(url, headers=headers)

def put_request(url, data):
    headers = {
        'Content-Type': 'application/vnd.api+json',
        'Authorization': 'Bearer {}'.format(OSF_TOKEN)
    }
    data = json.dumps(data)
    return requests.put(url, headers=headers, data=data)

#Call all nodes from stated user and save in dictionary of 'node_title' : 'node_id'
user_response = get_request(OSF_API_URL + 'users/' + USER_ID + '/nodes')
node_results = (user_response.json()['data'])

node_ids = {}
for node_result in node_results:
    title = (node_result['attributes']['title'])
    id = (node_result['id'])
    node_ids[title] = id
#print (node_ids)


#Call all wikis from each node and save in dictionary of node_title : wiki_name, wiki_download_link
wiki_info = {}
for k, v in node_ids.items():
    wiki_response = get_request(OSF_API_URL + 'nodes/' + v + '/wikis')
    wiki_results = (wiki_response.json()['data'])
    wiki_download_links = {}
    for wiki_result in wiki_results:
        name = wiki_result['attributes']['name']
        download_link = wiki_result['links']['download']
        wiki_download_links[name] = (download_link)
    wiki_info[k] = wiki_download_links
#print (wiki_info)

#Create/replace backups directory
dir = loc + 'OSF_backups/'
if os.path.exists(dir):
    shutil.rmtree(dir)
os.makedirs(dir)

#Create directory for each project in backups
for node_name, wiki_result_dict in wiki_info.items():
    dir = loc + 'OSF_backups/' + node_name
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)
    for wiki_name, wiki_url in wiki_result_dict.items():
        http_response = get_request(wiki_url)
        wiki_contents = http_response.text
        with open(dir + '/' + wiki_name + '.txt', 'w') as file:
            file.write(wiki_contents)
        

    

