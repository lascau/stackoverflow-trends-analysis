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



class DataAnalyzor:
    
    def __init__(self):
        start = time.time()
        self.df_answers = pd.read_csv(os.getcwd() + '/extracted_data/answers.csv')
        self.df_questions = pd.read_csv(os.getcwd() + '/extracted_data/questions.csv')
        self.df_comments = pd.read_csv(os.getcwd() + '/extracted_data/comments.csv')               
        end = time.time()
        print('Time to load csvs', end-start)
        
    def plot(self):
        start = time.time()
        root = tk.Tk()
        root.title('Stackoverflow trends analysis')
        
        # no. characters
        figure1 = plt.Figure(figsize=(6,5), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, root)
        bar1.get_tk_widget().place(x=0, y=5)
        ax1.set_title('Length of comments per days')
        self.strategy_length_comments_per_day(ax1)

        figure2 = plt.Figure(figsize=(6,5), dpi=100)
        ax2 = figure2.add_subplot(111)
        bar2 = FigureCanvasTkAgg(figure2, root)
        bar2.get_tk_widget().place(x=600,y=5)
        ax2.set_title('Length of answers per days')
        self.strategy_length_answers_per_day(ax2)

        figure3 = plt.Figure(figsize=(6,5), dpi=100)
        ax3 = figure3.add_subplot(111)
        bar3 = FigureCanvasTkAgg(figure3, root)
        bar3.get_tk_widget().place(x=1200,y=5)
        ax3.set_title('Length of questions per days')
        self.strategy_length_questions_per_day(ax3)
        
        # no. words
        figure4 = plt.Figure(figsize=(6,5), dpi=100)
        ax4 = figure4.add_subplot(111)
        bar4 = FigureCanvasTkAgg(figure4, root)
        bar4.get_tk_widget().place(x = 10, y = 500) 
        ax4.set_title('Number of words per days for comments')
        self.strategy_words_per_day_in_comments(ax4)

        figure5 = plt.Figure(figsize=(6,5), dpi=100)
        ax5 = figure5.add_subplot(111)
        bar5 = FigureCanvasTkAgg(figure5, root)
        bar5.get_tk_widget().place(x = 600, y = 500) 
        ax5.set_title('Number of words per days for answers')
        self.strategy_words_per_day_in_answers(ax5)

        figure6 = plt.Figure(figsize=(6,5), dpi=100)
        ax6 = figure6.add_subplot(111)
        bar6 = FigureCanvasTkAgg(figure6, root)
        bar6.get_tk_widget().place(x = 1200, y = 500) 
        ax6.set_title('Number of words per days for questions')
        self.strategy_words_per_day_in_questions(ax6)
        
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
        
