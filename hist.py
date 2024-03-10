from bs4 import BeautifulSoup
import requests
import pandas as pd

years = [1960,1964,1968,1972,1976,1980,1984,1988,1992,1996,2000,2004,2008,2012,2016,2020]

def get_matches(year):
    web = f'https://en.wikipedia.org/wiki/UEFA_Euro_{year}'
    response = requests.get(web)
    content = response.text
    soup = BeautifulSoup(content,'lxml')

    matches= soup.find_all('div','footballbox')

    home=[]
    score=[]
    away=[]
    for match in matches:
        home.append(match.find('th','fhome').get_text())
        score.append(match.find('th','fscore').get_text())
        away.append(match.find('th','faway').get_text())

    dict_football = {'Home':home,'Score':score,'Away':away}
    df_football=pd.DataFrame(dict_football)
    df_football['Year']=year
    return df_football

# historical data
uefa = [get_matches(year) for year in years]
df_uefa=pd.concat(uefa,ignore_index=True)
df_uefa.to_csv('euros_historical_data.csv',index=False)

# fixtures
df_fixtures = pd.DataFrame(get_matches('2024'))
print(df_fixtures)
df_fixtures.to_csv('euros_fixtures_data.csv',index=False)

