from scipy.stats import poisson
import pandas as pd
import pickle

dict_table=pickle.load(open('dict_table','rb'))
df_hist=pd.read_csv('euros_historical_data_clean.csv')
df_fixtures=pd.read_csv('euros_fixtures_data_clean.csv')

# splitting home and away tables
df_home = df_hist[['Home','Home Score','Away Score']]
df_away = df_hist[['Away','Home Score','Away Score']]
df_home=df_home.rename(columns={'Home': 'Team','Home Score': 'Goals For','Away Score': 'Goals Against'})
df_away=df_away.rename(columns={'Away': 'Team','Away Score': 'Goals For','Home Score': 'Goals Against'})

# get the average goals a team scores and concedes
df_home=df_home.rename(columns={'Home': 'Team','Home Score': 'Goals For','Away Score': 'Goals Against'})
df_rank=pd.concat([df_home,df_away],ignore_index=True).groupby('Team').mean()

# define a function to predict points
def predict_pts(home,away):
    if home in df_rank.index and away in df_rank.index:
        lamb_home=df_rank.at[home,'Goals For'] * df_rank.at[away,'Goals Against']
        lamp_away=df_rank.at[away,'Goals For'] * df_rank.at[home,'Goals Against']
        prob_home,prob_away,prob_draw = 0,0,0
        for x in range (0,11):
            for y in range (0,11):
                p=poisson.pmf(x,lamb_home) * poisson.pmf(y,lamp_away)
                if x == y:
                    prob_draw +=p
                elif x>y:
                    prob_home +=p
                else:
                    prob_away +=p
        points_home=3*prob_home+prob_draw
        points_away=3*prob_away+prob_draw
        return (points_home,points_away)
    else:
        return (0,0)

# split tournament into knockout and group phase
df_fixtures_group=df_fixtures[:36].copy()
df_fixtures_r16=df_fixtures[36:44].copy()
df_fixtures_quarter=df_fixtures[44:48].copy()
df_fixtures_semi=df_fixtures[48:50].copy()
df_fixtures_final=df_fixtures[50:].copy()

# simulate matches in gorup stage
for group in dict_table:
    print(dict_table[group]['Team'].values)

for group in dict_table:
    group_teams=dict_table[group]['Team'].values
    df_fixtures_group6=df_fixtures_group[df_fixtures_group['Home'].isin(group_teams)]
    for index,row in df_fixtures_group6.iterrows():
        home,away=row['Home'],row['Away']
        points_home,points_away=predict_pts(home,away)
        dict_table[group].loc[dict_table[group]['Team']== home,'Pts'] +=points_home
        dict_table[group].loc[dict_table[group]['Team']== away,'Pts'] +=points_away

    dict_table[group]=dict_table[group].sort_values('Pts',ascending=False).reset_index()
    dict_table[group]=dict_table[group][['Team','Pts']]
    dict_table[group]=dict_table[group].round(0)

# update round of 16 with group winners
for group in dict_table:
    group_winner=dict_table[group].loc[0,'Team']
    runner_up=dict_table[group].loc[1,'Team']
    group_DEF=dict_table['Group A'].loc[2,'Team']
    group_ADEF=dict_table['Group D'].loc[2,'Team']
    group_ABCD=dict_table['Group B'].loc[2,'Team']
    group_ABC=dict_table['Group C'].loc[2,'Team']

    df_fixtures_r16.replace({f'Winner {group}': group_winner,f'Runner-up {group}':runner_up,'3rd Group D/E/F':group_DEF,'3rd Group A/D/E/F':group_ADEF,'3rd Group A/B/C/D': group_ABCD,'3rd Group A/B/C': group_ABC},inplace=True)
    df_fixtures_r16['Winner'] = '?'

# function to determine a winner
def get_winner(df_fixture_winner):
    for index,row in df_fixture_winner.iterrows():
        home,away=row['Home'],row['Away']
        points_home,points_away=predict_pts(home,away)
        if points_home>points_away:
            winner=home
        else: 
            points_home<points_away
            winner=away
        df_fixture_winner.loc[index,'Winner'] = winner
    return df_fixture_winner

# Function to update table with winners
def updated_table(df_fixture_round_1,df_fixture_round_2):
    for index,row in df_fixture_round_1.iterrows():
        winner=df_fixture_round_1.loc[index,'Winner']
        match=df_fixture_round_1.loc[index,'Score']
        df_fixture_round_2.replace({f'Winner {match}':winner},inplace=True)
    df_fixture_round_2['Winner']='?'
    return df_fixture_round_2

# winners of quarter finals
updated_table(df_fixtures_r16,df_fixtures_quarter)
get_winner(df_fixtures_quarter)

# Semi-finals
updated_table(df_fixtures_quarter,df_fixtures_semi)
get_winner(df_fixtures_semi)

# Finals
updated_table(df_fixtures_semi,df_fixtures_final)
get_winner(df_fixtures_final)
