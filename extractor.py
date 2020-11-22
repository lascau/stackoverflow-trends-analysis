import requests # for doing http requests to a resource
import json # to serialize/deserialize the json getting from the call
import time # for delay with 2 s each api request
from requests.auth import HTTPBasicAuth
from datetime import datetime
import pandas as pd
import os
from json_debugger import JsonDebugger

class Extractor:

    def __init__(self, columns_names_list, json_keys_list):
        self.key = 'AzNRstImwHbaQF1FLdR6DQ(('
        self.columns_names_list = columns_names_list
        self.json_keys_list = json_keys_list
        self.columns_list = []
        for i in range(len(columns_names_list)):
            self.columns_list.append([])
        

    def extract_from(self, endpoint):
        for current_page in range(500):
            current_url = endpoint + str(current_page + 1) + '&key=' + self.key
            headers = {"Accept": "application/json"}
            auth = HTTPBasicAuth('apikey', self.key)
            response = requests.get(current_url, headers = headers, auth = auth)
    
            if response.status_code == requests.codes.ok:
                new_data = json.loads(response.text)
                if new_data['has_more'] is 'false':
                    break
                #debugger = JsonDebugger(response)
                #debugger.debug()
                for item in new_data['items']:
                    for json_key in self.json_keys_list:
                        index = self.json_keys_list.index(json_key)
                        if 'date' in json_key:
                            self.columns_list[index].append(datetime.fromtimestamp(item[json_key]))
                        elif 'tags' in json_key:
                            self.columns_list[index].append(' '.join(tag for tag in item[json_key]))
                        else:               
                            self.columns_list[index].append(item[json_key])
                print("Processed page " + str(current_page + 1) + ", returned " + str(response))
            else:
                print('Error:', response.status_code, response.content, sep = ' ')
            # timeout not to be rate-limited
            time.sleep(10)

    def export_to_csv(self, csv_name):
        current_directory = os.getcwd()
        extracted_data_directory = os.path.join(current_directory, r'extracted_data')
        if not os.path.exists(extracted_data_directory):
            os.makedirs(extracted_data_directory)


        data = pd.DataFrame(zip(*self.columns_list), 
                         columns = self.columns_names_list)
        data.to_csv('extracted_data/' + csv_name + '.csv')


if __name__ == '__main__':
    '''
    questions_extractor = Extractor(['Title', 'Content', 'Creation Date', 'Tags'], ['title', 'body_markdown', 'creation_date', 'tags'])
    questions_extractor.extract_from('https://api.stackexchange.com/2.2/questions?order=desc&sort=activity&site=stackoverflow&pagesize=100&filter=!9_bDDx5MI&page=')
    questions_extractor.export_to_csv('questions')
    '''
    answers_extractor = Extractor(['Answer', 'Creation Date'], ['body_markdown', 'creation_date'])
    answers_extractor.extract_from('https://api.stackexchange.com/2.2/answers?order=desc&sort=activity&site=stackoverflow&pagesize=100&filter=!9_bDE(S6I&page=')
    answers_extractor.export_to_csv('answers')

    '''
    comments_extractor = Extractor(['Comment', 'Creation Date'], ['body', 'creation_date'])
    comments_extractor.extract_from('https://api.stackexchange.com/2.2/comments?order=desc&sort=creation&site=stackoverflow&pagesize=100&filter=!9_bDE0E4s&page=')
    comments_extractor.export_to_csv('comments')
    '''
