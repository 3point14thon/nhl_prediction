import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

#gives the number of NaNs in a column
def nanCount(df):
  for column in df.columns:
    print str(df[column].isnull().sum().sum()) + ' nans in ' + column


#Note that this csv file does NOT contain statistics pertaining to goalies
def formatCSV():
  df = pd.read_csv('hky_stats.csv')
  df['flPoints'] = df.goals*3.0 + df.shots*0.1 + df.assists*2 + df.ppPoints + df.shPoints*2
  y = df['flPoints']
  df = df.drop(['Unnamed: 0','gamesPlayed','gameId','playerBirthCity','playerBirthCountry','playerId','playerBirthStateProvince','playerFirstName','playerLastName','playerNationality','flPoints'],axis=1)
  #sepparating out features I want to deal with later, figure out if timeOnIcePerGame is an average of all games or per the game in question
  df = df.drop(['assists','gameWinningGoals','goals','otGoals','penaltyMinutes','plusMinus','points','ppGoals','ppPoints','shGoals','shPoints','shiftsPerGame','shootingPctg','shots','timeOnIcePerGame'], axis=1)
  NanColumns = df[['playerDraftOverallPickNo','playerDraftRoundNo','playerDraftYear']]
  df = df.drop(['faceoffWinPctg','playerDraftOverallPickNo','playerDraftRoundNo','playerDraftYear','playerHeight','playerWeight','playerInHockeyHof','playerIsActive'],axis=1)
  df.gameDate = pd.to_datetime(df.gameDate)
  df.playerBirthDate = pd.to_datetime(df.playerBirthDate)
  #print nanCount(dates)
  #cat = pd.get_dummies(cat)
  nanCount(df)
  FillEDA(NanColumns,y)
  print NanColumns.head()

def FillEDA(X,y):
  X['scores'] = y
  X.dropna()
  y = X.scores
  X = X.drop(['scores'],axis=1)
  for column in X.columns:
    plt.figure()
    plt.scatter(X[column],y)
    plt.title(column)
  plt.show()
formatCSV()

