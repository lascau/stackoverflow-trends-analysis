import requests # for doing http requests to a resource
import json # to serialize/deserialize the json getting from the call
import time # for delay with 2 s each api request
from requests.auth import HTTPBasicAuth


key = 'AzNRstImwHbaQF1FLdR6DQ(('

question_title = []
questions_content = []
for current_page in range(1):
    url = 'https://api.stackexchange.com/2.2/questions?order=desc&sort=activity&site=stackoverflow&pagesize=100&filter=!9_bDDx5MI&page='+ str(current_page + 1)
    headers = {"Accept": "application/json"}
    auth = HTTPBasicAuth('apikey', 'AzNRstImwHbaQF1FLdR6DQ((')
    response = requests.get(url, headers = headers, auth = auth)
    
    if response.status_code == requests.codes.ok:
        newData = json.loads(response.text)
        '''
        Identation of the json response
        '''
        result_json = response.json()
        # convert our json to str type
        json_str = json.dumps(result_json)

        json_object = json.loads(json_str)    
   
        # Difference in the spaces  
        # near the brackets can be seen 
        print(json.dumps(json_object, indent = 3)) 

        for item in newData['items']:
            question_title.append(item['title'])
            questions_content.append(item['body_markdown'])
        print("Processed page " + str(current_page + 1) + ", returned " + str(response))
        # timeout not to be rate-limited
        time.sleep(2)
    else:
        print('Error:', response.status_code, sep = ' ')

'''
#Debug
for title, content in zip(question_title, questions_content):
    print(f'Title is: {title}\nContent is: {content}')
'''
