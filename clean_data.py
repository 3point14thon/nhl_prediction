import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

def main():
  #Note that this csv file does NOT contain statistics pertaining to goalies
  df = pd.read_csv('hky_stats.csv')
  df['flPoints'] = df.goals*3.0 + df.shots*0.1 + df.assists*2 + df.ppPoints + df.shPoints*2
  df.gameDate = pd.to_datetime(df.gameDate)
  df.playerBirthDate = pd.to_datetime(df.playerBirthDate)
  BirthNDraft = df[['playerName','playerBirthDate','playerDraftYear','flPoints']]
  # Filling draft number and round with the means of thier columns
  #FillEDA(NanColumns,y)
  NanColumns = df[['playerDraftOverallPickNo','playerDraftRoundNo']]
  for column in NanColumns.columns:
    df[column].fillna(NanColumns[column].mean(),inplace=True)
  #BirthyearVDraftyear(BirthNDraft)
  #print nanCount(df)
  #GameDataEDA(df,'penaltyMinutes')
  #df = drop(df)
  df = df.sort_values('gameDate')
  graphTOI(df,'penaltyMinutes')
  #for player in df.playerName.drop_duplicates():
   # PlayerGames = df[df.playerName==player]
    #df.loc[df.playerName==player, 'timeOnIcePerGame'] = PlayerGames.timeOnIcePerGame.rolling(5).mean()
  df.to_csv('clean_hky_stats.csv',encoding='utf-8')
  
def graphTOI(df,feature):
  i = 0
  c = ['r','g','b','y']
  positions = df.playerPositionCode.drop_duplicates()
  plt.figure()
  for position in positions:
    PositionDf = df[df.playerPositionCode==position]
    plt.scatter(PositionDf[feature],PositionDf.flPoints,color=c[i])
    i += 1
  plt.legend(positions)
  plt.show()

def GameDataEDA(X, feature):
  names = X.playerName.drop_duplicates().iloc[:3]
  for name in names:
    PlayerStat = X[X.playerName==name].sort_values(by='gameDate')
    PlayerStat.index = range(len(PlayerStat))
    for i in PlayerStat.index:
      PlayerStat.at[i,'average'] = PlayerStat[feature].iloc[:i].mean()
    PlayerStat['rollingAvg'] = PlayerStat[feature].rolling(5).mean()
    PlayerStat['rollingAvg3'] = PlayerStat[feature].rolling(3).mean()
    plt.figure()
    plt.scatter(PlayerStat.gameDate,PlayerStat.rollingAvg3,color='y')
    plt.scatter(PlayerStat.gameDate,PlayerStat.rollingAvg,color='g')
    plt.scatter(PlayerStat.gameDate,PlayerStat.average,color='r')
    plt.scatter(PlayerStat.gameDate,PlayerStat[feature])
    plt.title(name)
    plt.figure()
    plt.scatter(PlayerStat.flPoints,PlayerStat.rollingAvg3,color='y')
    plt.scatter(PlayerStat.flPoints,PlayerStat.rollingAvg,color='g')
    plt.scatter(PlayerStat.flPoints,PlayerStat.average,color='r')
    plt.scatter(PlayerStat.flPoints,PlayerStat[feature])
    plt.title(name)
  plt.show()

# Takes in the main data frame and returns a streamlined dataframe
def drop(X):
  #droping unnecisary features, redundent features, or features directly related   to the target variable
  X = X.drop(['Unnamed: 0','gamesPlayed','gameId','playerBirthCity','playerBirthCountry','plusMinus','playerId','playerBirthStateProvince','shootingPctg','playerFirstName','playerLastName','playerNationality','playerDraftYear''assists','gameWinningGoals','goals','otGoals','points','ppGoals','ppPoints','shGoals','shPoints'],axis=1) 
  #sepparating out features I want to deal with later, figure out if timeOnIcePerGame is an average of all games or per the game in question
#  X = X.drop(['penaltyMinutes','shiftsPerGame','shots','timeOnIcePerGame'], axis=1)
  return X

#gives the number of NaNs in every column in a Data frame
def nanCount(df):
  for column in df.columns:
    print str(df[column].isnull().sum().sum()) + ' nans in ' + column

# Performs some baisic EDA to determine if nan columns are worth keeping 
def FillEDA(X):
  naX = X[X.isnull()]
  plt.figure()
  plt.hist(flPoints)
  X.dropna()
  y = X.scores
  X = X.drop(['scores'],axis=1)
  for column in X.columns:
    plt.figure()
    plt.scatter(X[column],X.flPoints)
    plt.title(column)
  plt.show()

# takes in a dataframe containing playername, playerbirthdate, and flpoints and
# plots both draftyear and birthyear vs flpoints on a scatterplot
def BirthyearVDraftyear(X):
  #translates birth year for a better comparison
  X['playerBirthDate'] = X.playerBirthDate.dt.year + 18 
  plt.figure()
  plt.scatter(X.playerDraftYear,X.flPoints,alpha=0.5)
  plt.scatter(X.playerBirthDate,X.flPoints,color='r',alpha=0.5)
  plt.title('Birth year and Draft year vs FL points')
  plt.xlabel('Year')
  plt.ylabel('FL points')
  plt.xlim([1988,2018])
  plt.ylim([0,17])
  plt.show()

main()
