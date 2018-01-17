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
  similarMetrics = df[['goals','gameWinningGoals','otGoals','ppGoals','shGoals','points','shPoints','ppPoints']]
  #print nanCount(df)

# Takes in the main data frame and returns a streamlined dataframe
def drop(X):
  #droping unnecisary or redundent features
  df = df.drop(['Unnamed: 0','gamesPlayed','gameId','playerBirthCity','playerBirthCountry','plusMinus','playerId','playerBirthStateProvince','shootingPctg','playerFirstName','playerLastName','playerNationality','playerDraftYear'],axis=1) 
  #sepparating out features I want to deal with later, figure out if timeOnIcePerGame is an average of all games or per the game in question
  #df = df.drop(['assists','gameWinningGoals','goals','otGoals','penaltyMinutes','points','ppGoals','ppPoints','shGoals','shPoints','shiftsPerGame','shots','timeOnIcePerGame'], axis=1)
  return df

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
