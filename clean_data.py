import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

def main():
  '''
  Generates a csv file containing cleaned data.

  Returns: None
  '''
  #Note that this csv file does NOT contain statistics pertaining to goalies
  df = pd.read_csv('hky_stats.csv')
  df['flPoints'] = df.goals*3.0 + df.shots*0.1 + df.assists*2 + df.ppPoints + df.shPoints*2
  df.gameDate = pd.to_datetime(df.gameDate)
  df.playerBirthDate = pd.to_datetime(df.playerBirthDate)
  BirthNDraft = df[['playerName','playerBirthDate','playerDraftYear','flPoints']]
  NanColumns = df[['playerDraftOverallPickNo','playerDraftRoundNo']]
  for column in NanColumns.columns:
    df[column].fillna(NanColumns[column].mean(),inplace=True)
  df = drop(df)
  df = df.sort_values('gameDate')
  df['rolling_toi'] = RollingAvgFill(df,'timeOnIcePerGame')
  df['rolling_penalty_min'] = RollingAvgFill(df,'penaltyMinutes')
  df['rolling_spg'] = RollingAvgFill(df,'shiftsPerGame')
  df = df.dropna(axis=0)
  df.to_csv('clean_hky_stats.csv',encoding='utf-8')

#it might be a better idea to use another model for the values rollingavgfill would deal with
def rolling_avg_fill(df,feature):
  '''
  This function sorts through df and uses a running average for the expected value
  of an attribute for the next game if a player has played in fewer than insert variable here
  games. Otherwise  it passes a rolling average of the past three instances of the attribute.

  Args:
    df: dataframe containing the specified feature
    feature: the feature to have the rolling avg applied to

  Returns:
    newdf:

  '''
  newdf = pd.DataFrame()
  for player in df.playerName.drop_duplicates():
    PlayerGames = df[df.playerName==player]
    PlayerGames.index = range(len(PlayerGames))
    if 1 >= len(PlayerGames):
      PlayerGames.loc[:,feature] = np.nan
    elif 5 > len(PlayerGames):
      PlayerGames.index = range(len(PlayerGames))
      for i in PlayerGames.index:
        PlayerGames.loc[i,'ravg'] = PlayerGames.loc[:i,feature].mean()
      rollingmean = PlayerGames.ravg
      PlayerGames = PlayerGames.drop('ravg',axis=1)
    else:
      rollingmean = PlayerGames[feature].rolling(3).mean()
      rollingmean.iloc[:2] = PlayerGames[feature].iloc[:2]
    rollingmean.loc[-1] = np.nan
    rollingmean = rollingmean.drop(len(rollingmean)-2,axis=0)
    rollingmean = rollingmean.sort_index()
    df.loc[df.playerName==player, feature] = rollingmean# currently only puts in nan values
    PlayerGames[feature+'OffSet'] = rollingmean
    newdf = newdf.append(PlayerGames)
    newdf = newdf.drop(feature,axis=1)
  return newdf

def graph_toi(df,feature):
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

def game_dat_eda(X, feature):
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
  print PlayerStat[['penaltyMinutes','rollingAvg3']]
  plt.show()

# Takes in the main data frame and returns a streamlined dataframe
def drop(X):
  #droping unnecisary features, redundent features, or features directly related   to the target variable
  X = X.drop(['Unnamed: 0','gamesPlayed','gameId','playerBirthCity','playerBirthCountry','plusMinus','playerId','playerBirthStateProvince','shootingPctg','playerFirstName','playerLastName','playerNationality','playerDraftYear','assists','gameWinningGoals','goals','otGoals','points','ppGoals','ppPoints','shGoals','shPoints'],axis=1) 
  #sepparating out features I want to deal with later, figure out if timeOnIcePerGame is an average of all games or per the game in question
#  X = X.drop(['penaltyMinutes','shiftsPerGame','shots','timeOnIcePerGame'], axis=1)
  return X

# Performs some baisic EDA to determine if nan columns are worth keeping
def fill_eda(X):
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
def birth_year_draft_year(X):
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

if __name__ == '__main__':
  main()

