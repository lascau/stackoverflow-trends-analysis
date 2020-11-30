import pandas as pd
import os
import html # for unescape html
import nltk

class Parser:

    def __init__(self):
        pass

    def parse(self):
        data_answers = pd.read_csv(os.getcwd() + '/extracted_data/answers.csv')
        data_comments = pd.read_csv(os.getcwd() + '/extracted_data/comments.csv')
        data_questions = pd.read_csv(os.getcwd() + '/extracted_data/questions.csv')
        tokens = [html.unescape(tok).split() for tok in data_answers['Answer'].head(10)]
        print(tokens)
        
    def export_to_csv(self):
        pass

if __name__ == '__main__':
    parser = Parser()
    parser.parse()
    parser.export_to_csv()
    #help(nltk)

