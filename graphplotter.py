import pandas as pd
from pandas import DataFrame
import os
import tkinter as tk
import datetime
import calendar # for converting index month to name calendar.month_name[idx]
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor


class DataAnalyzor:

    def convert(self, df, column_name):
        return pd.to_datetime(df[column_name],
                              format='%Y-%m-%d %H:%M:%S')

    def read_answers(self):
        self.df_answers   = pd.read_csv(os.getcwd() + '/extracted_data/answers.csv', usecols=['Answer', 'Creation Date'])

    def read_questions(self):
        self.df_questions = pd.read_csv(os.getcwd() + '/extracted_data/questions.csv', usecols=['Title', 'Content', 'Creation Date', 'Tags'])

    def read_comments(self):
        self.df_comments  = pd.read_csv(os.getcwd() + '/extracted_data/comments.csv', usecols=['Comment', 'Creation Date'])
    
    def __init__(self):
        start = time.time()
             
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.submit(self.read_answers)
            executor.submit(self.read_questions)
            executor.submit(self.read_comments)

        self.df_answers['Creation Date'] = self.convert(self.df_answers, 'Creation Date')
        self.df_comments['Creation Date'] = self.convert(self.df_comments, 'Creation Date')
        self.df_questions['Creation Date'] = self.convert(self.df_questions, 'Creation Date')

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
        root.state('zoomed')
        root.title('Stackoverflow trends analysis')
    
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
        

        for pos_x, pos_y, title, strategy in zip(self.window_xposes,
                                                 self.window_yposes,
                                                 self.titles,
                                                 self.strategies):
            self.draw_strategy(root, pos_x, pos_y, title, strategy)

        
        end = time.time()
        print('Time to load plots:', end - start)
        root.mainloop()

    def strategy_length_answers_per_day(self, ax):

        data = {'Length of answer' : self.df_answers['Answer']
                                                         .map(lambda answer: len(answer))
                                                         .tolist(),
                'Days'            : self.df_answers['Creation Date']
                                                              .map(lambda date: date.day)
                                                              .tolist()
                }
        df = DataFrame(data, columns = ['Length of answer', 'Days'])
        df.plot(x = 'Days', y = 'Length of answer', kind = 'scatter', ax = ax)
        plt.show()

    def strategy_length_comments_per_day(self, ax):
        
        data = {'Length of comment' : self.df_comments['Comment']
                                                         .map(lambda comment: len(comment))
                                                         .tolist(),
                'Days'            : self.df_comments['Creation Date']
                                                              .map(lambda date: date.day)
                                                              .tolist()
                }
        df = DataFrame(data, columns = ['Length of comment', 'Days'])
        df.plot(x = 'Days', y = 'Length of comment', color='y', kind = 'scatter', ax = ax)
        plt.show()

    def strategy_length_questions_per_day(self, ax):
        
        data = {'Length of question' : self.df_questions['Title']
                                                         .map(lambda comment: len(comment))
                                                         .tolist(),
                'Days'            : self.df_questions['Creation Date']
                                                              .map(lambda date: date.day)
                                                              .tolist()
                }
        df = DataFrame(data, columns = ['Length of question', 'Days'])
        df.plot(x = 'Days', y = 'Length of question', color='r', kind = 'scatter', ax = ax)
        plt.show()

    def strategy_words_per_day_in_comments(self, ax):

        data = {'Number of words' : self.df_comments['Comment']
                                                         .map(lambda comment: len(comment.split(' ')))
                                                         .tolist(),
                'Days'            : self.df_comments['Creation Date']
                                                              .map(lambda date: date.day)
                                                              .tolist()
                }
        df = DataFrame(data, columns = ['Number of words', 'Days'])
        df.plot(x = 'Days', y = 'Number of words', kind = 'scatter', ax = ax)
        plt.show()
    
    def strategy_words_per_day_in_answers(self, ax):

        data = {'Number of words' : self.df_answers['Answer']
                                                         .map(lambda answer: len(answer.split(' ')))
                                                         .tolist(),
                'Days'            : self.df_answers['Creation Date']
                                                              .map(lambda date: date.day)
                                                              .tolist()
                }
        df = DataFrame(data, columns = ['Number of words', 'Days'])
        df.plot(x = 'Days', y = 'Number of words', kind = 'scatter', ax = ax)
        plt.show()
        
    
    def strategy_words_per_day_in_questions(self, ax):

        data = {'Number of words' : self.df_questions['Title']
                                                         .map(lambda comment: len(comment.split(' ')))
                                                         .tolist(),
                'Days'            : self.df_questions['Creation Date']
                                                              .map(lambda date: date.day)
                                                              .tolist()
                }
        df = DataFrame(data, columns = ['Number of words', 'Days'])
        df.plot(x = 'Days', y = 'Number of words', kind = 'scatter', ax = ax)
        plt.show()

    


if __name__ == '__main__':
    data_analyzor = DataAnalyzor()
    data_analyzor.plot()
        
