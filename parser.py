import pandas as pd
import os
import html # for unescape html
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.tree import Tree
import itertools
import time


class Parser:

    def __init__(self):
        pass

    def parse(self):
        data_answers = pd.read_csv(os.getcwd() + '/extracted_data/answers.csv')
        data_comments = pd.read_csv(os.getcwd() + '/extracted_data/comments.csv')
        data_questions = pd.read_csv(os.getcwd() + '/extracted_data/questions.csv')
        
        tokenizer = nltk.RegexpTokenizer(r"\w+")
        full_text = ''.join(data_answers['Answer'].head(2))
        #print(full_text)
        words = [word_tokenize(html.unescape(' '.join(tokenizer.tokenize(word)))) for word in data_answers['Answer'].head(10)]
        #print(words)
        '''
        #it takes to much time when all answers are merged
        words = list(itertools.chain.from_iterable(words))
        '''
        for word in words:
            #start time
            tic = time.perf_counter()

            tagged = nltk.pos_tag(word)
            #end time
            toc = time.perf_counter()
            print(f"Time : {(toc - tic)*60:0.4f} seconds")

            # it takes much more time when we have a huge number of tagged words to deal with
            pattern = "NP: {<DT>?<JJ>*<NN>}"
            tagged = list(map(lambda sent: Tree(sent[1], children=[sent[0]]), tagged))
            NPChunker = nltk.RegexpParser(pattern) 
            result = NPChunker.parse(tagged)
            result.draw()

        
    def export_to_csv(self):
        pass

if __name__ == '__main__':
    parser = Parser()
    parser.parse()
    parser.export_to_csv()
    #help(nltk)

