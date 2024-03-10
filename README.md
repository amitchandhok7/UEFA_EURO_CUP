# UEFA_EURO_CUP_2024_PREDICTION

Hi,

Welcome to my project, where I bridge the gap between hobbies and learning opportunities. Being an avid soccer fan since 2005, I have watched thousands of games and made (biased) predictions for each one, some being correct and some being incorrect. With this project, I hope to take this fandom one step furthur and use statistical modelling to predict the winner of the upcoming UEFA Euro Cup. 

To complete this project, I utilized Python with the following libraries:
- Pandas
- SciPy
- String
- BeautifulSoup
- Requests
- Pickle

To summarize this process, I:
- Imported all the fixtures of the tournament and historcial data for each team through web scrapping
- Cleaned data using Pandas to normalize columns and remove inconistent values
- Created a dictionary to store all fixtures along with an added "Winner" column
- Used Poisson distributuon to calculate the probability of each team progressing in the tournament
- Built a model using the Pandas and SciPy libraries to predict the winners of each game and update the dictionary

From this excercise, I believe Italy will win the Euro Cup in 2024.

Thank you for reading.

Amit
