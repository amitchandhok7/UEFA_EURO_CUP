import pandas as pd

df_hist=pd.read_csv('euros_historical_data.csv')
df_fixtures=pd.read_csv('euros_fixtures_data.csv')

# removed all blanks
df_fixtures['Home']=df_fixtures['Home'].str.strip()
df_fixtures['Away']=df_fixtures['Away'].str.strip()
df_hist['Home']=df_hist['Home'].str.strip()
df_hist['Away']=df_hist['Away'].str.strip()

# no nulls exist
df_hist[df_hist['Home'].isnull()]
df_hist[df_hist['Away'].isnull()]

# drop duplicates
df_hist.drop_duplicates(inplace=True)
df_hist.sort_values('year',inplace=True)

# drop non numerical scores
df_hist['Score']=df_hist['Score'].str.replace('[/.^abcdefghijklmnopqrstuvwxyzI() ]','',regex=True)

# split score column into 2 columns
df_hist[['Home Score','Away Score']]=df_hist['Score'].str.split('–',expand=True)
df_hist.drop('Score',axis=1,inplace=True)

# renaming title headings
df_hist.rename(columns={'year':'Year'},inplace=True)
df_fixtures.rename(columns={'year':'Year'},inplace=True)

# changing the data type of column
df_hist=df_hist.astype({'Home Score':int,'Year':int,'Away Score': int})
df_fixtures=df_fixtures.astype({'Year':int})

# adding a column for total goals
df_hist['Total Score']=df_hist['Home Score']+df_hist['Away Score']

df_hist.to_csv('euros_historical_data_clean.csv',index=False)
df_fixtures.to_csv('euros_fixtures_data_clean.csv',index=False)
