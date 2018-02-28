import pandas as pd
#import joblib don't have this librairy yet 
from sklearn import preprocessing
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline

def main():
  df = pd.read_csv('clean_hky_stats.csv')
  df = df.drop('Unnamed: 0',axis=1)
  df.gameDate = pd.to_datetime(df.gameDate)
  df.playerBirthDate = pd.to_datetime(df.playerBirthDate)
  df = df.sort_values(by='gameDate')
  df = df.reset_index(drop=True)
  #df = df.drop(['playerBirthDate','gameDate'],axis=1)
  df = encode(df)
  
  #Train/Test Split
  TsPercent = 0.3
  df['playerBirthDate'] = df['playerBirthDate'].apply(lambda x: x.toordinal())
  df['gameDate'] = df['gameDate'].apply(lambda x: x.toordinal())
  Train = df.iloc[:int(len(df)*(1-TsPercent))]
  Test = df.iloc[int(len(df)*(1-TsPercent)):]
  yTrain = Train.flPoints
  yTest = Test.flPoints
  #setting up labels for sub models
  yTrainTOI = Train.timeOnIcePerGame
  yTestTOI = Test.timeOnIcePerGame
  yTrainPM = Train.penaltyMinutes
  yTestSPG = Test.shiftsPerGame
  yTrainSPG = Train.shiftsPerGame
  XTrain = Train.drop(['flPoints','timeOnIcePerGame','penaltyMinutes','shiftsPerGame'],axis=1)
  XTest = Test.drop(['flPoints','timeOnIcePerGame','penaltyMinutes','shiftsPerGame'],axis=1)
  #model: time on ice per game
  #using OLS to begin with because it's easy and quick
  OLS = LinearRegression()
  backcheck(XTrain,yTrainTOI,OLS)
  pp = preprocessing.Normalizer()
  pp.fit(XTrain)
  XTrain = pp.transform(XTrain)
  XTest = pp.transform(XTest)
  svr = SVR()
  parameters = {'kernel':('linear','rbf'),'C':(0.001,0.01,0.1,1,10,100,1000),
                'gamma':(0.00001,0.0001,0.001,0.01,0.1,1,10),
                'epsilon':(0.0001,0.001,0.01,0.1,1)}
  print 'Generateing model, this may take a while'
  model = GridSearchCV(svr,parameters)
  model.fit(XTrain,yTrain)
  joblib.dump(model,'SVR_model.pkl')
  print model.get_params()
  #model.score(XTest,yTest)

def encode(df):
  df = pd.get_dummies(df,columns=['opponentTeamAbbrev','playerName',
                                  'playerPositionCode','teamAbbrev'])
  df.playerShootsCatches = df.playerShootsCatches.map({'R':1,'L':0})
  return df

def backcheck(X,y,model):
  splits =TimeSeriesSplit(n_splits=3)
  for TrainIndex, TestIndex in splits.split(X):
    XTrain = X.iloc[TrainIndex,:]
    XTest = X.iloc[TestIndex,:]
    yTrain = y.iloc[TrainIndex]
    yTest = y.iloc[TestIndex]
    model.fit(XTrain,yTrain)
    print model.score(XTest,yTest)

  print(cross_val_score(OLS,XTrain,yTrainTOI))# cross validation wont work because it's a time series


main()
