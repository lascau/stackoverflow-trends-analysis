import pandas as pd
from pandas import DataFrame
import os
import tkinter as tk
import datetime
import calendar # for converting index month to name calendar.month_name[idx]
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import BOTTOM
import time
import concurrent.futures

class DataAnalyzor:
    
    def __init__(self):
        start = time.time()
        # data frames
        self.df_answers = pd.read_csv(os.getcwd() + '/extracted_data/answers.csv')
        self.df_questions = pd.read_csv(os.getcwd() + '/extracted_data/questions.csv')
        self.df_comments = pd.read_csv(os.getcwd() + '/extracted_data/comments.csv')               
        end = time.time()
        print('Time to load csvs', end-start)

    def draw_strategy(self, root, pos_x, pos_y, title, strategy):
        figure = plt.Figure(figsize=(6,5), dpi=100)
        ax = figure.add_subplot(111)
        bar = FigureCanvasTkAgg(figure, root)
        bar.get_tk_widget().place(x = pos_x, y = pos_y)
        ax.set_title(title)
        strategy(ax)  
       
    def plot(self):
        start = time.time()
        root = tk.Tk()
        root.title('Stackoverflow trends analysis')
    
         # info for doing concurency
        self.strategies = [
                            self.strategy_length_comments_per_day,
                            self.strategy_length_answers_per_day,
                            self.strategy_length_questions_per_day,

                            self.strategy_words_per_day_in_comments,
                            self.strategy_words_per_day_in_answers,
                            self.strategy_words_per_day_in_questions
                            
                          ]
        self.window_xposes = [0, 600, 1200, 10, 600, 1200]
        self.window_yposes = [5, 6, 5, 500, 500, 500]
        self.titles = ['Length of comments per days',
                       'Length of answers per days',
                       'Length of questions per days',
                       'Number of words per days for comments',
                       'Number of words per days for answers',
                       'Number of words per days for answers']
        
        #with concurent.futures.ProcessPoolExecutor() as executor:
        for pos_x, pos_y, title, strategy in zip(self.window_xposes,
                                                     self.window_yposes,
                                                     self.titles,
                                                     self.strategies):
            self.draw_strategy(root, pos_x, pos_y, title, strategy)

        
        end = time.time()
        print('Time to load plots:', end - start)
        root.mainloop()

    def strategy_length_answers_per_day(self, ax):
        #Answer, Creation Date
        data = {'Length of answer' : self.df_answers['Answer']
                                                         .map(lambda answer: len(answer))
                                                         .tolist(),
                'Days'            : self.df_answers['Creation Date']
                                                              .map(lambda date: datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").day)
                                                              .tolist()
                }
        df = DataFrame(data, columns = ['Length of answer', 'Days'])
        df.plot(x = 'Days', y = 'Length of answer', kind = 'scatter', ax = ax)
        #print(data['Length of answer'])
        plt.show()

    def strategy_length_comments_per_day(self, ax):
        #Comment, Creation Date
        data = {'Length of comment' : self.df_comments['Comment']
                                                         .map(lambda comment: len(comment))
                                                         .tolist(),
                'Days'            : self.df_comments['Creation Date']
                                                              .map(lambda date: datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").day)
                                                              .tolist()
                }
        df = DataFrame(data, columns = ['Length of comment', 'Days'])
        df.plot(x = 'Days', y = 'Length of comment', color='y', kind = 'scatter', ax = ax)
        #print(data['Length of answer'])
        plt.show()

    def strategy_length_questions_per_day(self, ax):
        
        #Title Content, Creation Date, Tags
        data = {'Length of question' : self.df_questions['Title']
                                                         .map(lambda comment: len(comment))
                                                         .tolist(),
                'Days'            : self.df_questions['Creation Date']
                                                              .map(lambda date: datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").day)
                                                              .tolist()
                }
        df = DataFrame(data, columns = ['Length of question', 'Days'])
        df.plot(x = 'Days', y = 'Length of question', color='r', kind = 'scatter', ax = ax)
        #print(data['Length of answer'])
        plt.show()

    def strategy_words_per_day_in_comments(self, ax):
        #Comment, Creation Date
        data = {'Number of words' : self.df_comments['Comment']
                                                         .map(lambda comment: len(comment.split(' ')))
                                                         .tolist(),
                'Days'            : self.df_comments['Creation Date']
                                                              .map(lambda date: datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").day)
                                                              .tolist()
                }
        df = DataFrame(data, columns = ['Number of words', 'Days'])
        df.plot(x = 'Days', y = 'Number of words', kind = 'scatter', ax = ax)
        #print(data['Length of answer'])
        plt.show()
    
    def strategy_words_per_day_in_answers(self, ax):
        df_answers = pd.read_csv(os.getcwd() + '/extracted_data/answers.csv')
        #Answer, Creation Date
        data = {'Number of words' : self.df_answers['Answer']
                                                         .map(lambda answer: len(answer.split(' ')))
                                                         .tolist(),
                'Days'            : self.df_answers['Creation Date']
                                                              .map(lambda date: datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").day)
                                                              .tolist()
                }
        df = DataFrame(data, columns = ['Number of words', 'Days'])
        df.plot(x = 'Days', y = 'Number of words', kind = 'scatter', ax = ax)
        #print(data['Length of answer'])
        plt.show()
        
    
    def strategy_words_per_day_in_questions(self, ax):

        #Title Content, Creation Date, Tags
        data = {'Number of words' : self.df_questions['Title']
                                                         .map(lambda comment: len(comment.split(' ')))
                                                         .tolist(),
                'Days'            : self.df_questions['Creation Date']
                                                              .map(lambda date: datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").day)
                                                              .tolist()
                }
        df = DataFrame(data, columns = ['Number of words', 'Days'])
        df.plot(x = 'Days', y = 'Number of words', kind = 'scatter', ax = ax)
        #print(data['Length of answer'])
        plt.show()

    


if __name__ == '__main__':
    data_analyzor = DataAnalyzor()
    data_analyzor.plot()
        
