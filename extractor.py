import requests # for doing http requests to a resource
import json # to serialize/deserialize the json getting from the call
import time # for delay with 2 s each api request
from requests.auth import HTTPBasicAuth
from datetime import datetime
import pandas as pd
import os
from json_debugger import JsonDebugger

key = 'AzNRstImwHbaQF1FLdR6DQ(('

question_title = []
question_content = []
question_creation_date = []

for current_page in range(1):
    url = 'https://api.stackexchange.com/2.2/questions?order=desc&sort=activity&site=stackoverflow&pagesize=100&filter=!9_bDDx5MI&page='+ str(current_page + 1)
    headers = {"Accept": "application/json"}
    auth = HTTPBasicAuth('apikey', 'AzNRstImwHbaQF1FLdR6DQ((')
    response = requests.get(url, headers = headers, auth = auth)
    
    if response.status_code == requests.codes.ok:
        newData = json.loads(response.text)
        debugger = JsonDebugger(response)
        debugger.debug()
        for item in newData['items']:
            question_title.append(item['title'])
            question_content.append(item['body_markdown'])
            question_creation_date.append(datetime.fromtimestamp(item['creation_date']))
        print("Processed page " + str(current_page + 1) + ", returned " + str(response))
        # timeout not to be rate-limited
        time.sleep(2)
    else:
        print('Error:', response.status_code, sep = ' ')

current_directory = os.getcwd()
extracted_data_directory = os.path.join(current_directory, r'extracted_data')
if not os.path.exists(extracted_data_directory):
    os.makedirs(extracted_data_directory)


questions_dataframe = pd.DataFrame(list(zip(question_title, question_content, question_creation_date)), 
                         columns = ['Title', 'Content', 'Creation Date'])
questions_dataframe.to_csv('extracted_data/questions.csv')

'''
#Debug
for title, content in zip(question_title, question_content):
    print(f'Title is: {title}\nContent is: {content}')
for d in question_creation_date:
    print(f'My date: {d}')
'''


