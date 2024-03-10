import pandas as pd
from string import ascii_uppercase as alphabet
import pickle

all_tables= pd.read_html('https://en.wikipedia.org/wiki/UEFA_Euro_2024')

dict_table={}
for letter,i in zip(alphabet,range(9,51,7)):
    df=all_tables[i]
    df.rename(columns={df.columns[1]:'Team'},inplace=True)
    df.pop('Qualification')
    df.replace('Play-off winner A','Wales',inplace=True)
    df.replace('Play-off winner B','Iceland',inplace=True)
    df.replace('Play-off winner C','Georgia',inplace=True)
    df.replace('Germany (H)','Germany',inplace=True)
    dict_table[f'Group {letter}']=df

with open ('dict_table','wb') as output:
    pickle.dump(dict_table,output)

