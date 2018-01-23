import pandas as pd
import joblib 
from sklearn import preprocessing
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV

def main():
  df = pd.read_csv('clean_hky_stats.csv')
  df = df.drop('Unnamed: 0',axis=1)
  df.gameDate = pd.to_datetime(df.gameDate)
  df.playerBirthDate = pd.to_datetime(df.playerBirthDate)
  df = df.sort_values(by='gameDate')
  df = df.reindex()
  #df = df.drop(['playerBirthDate','gameDate'],axis=1)
  print df.dtypes
  df = encode(df)
  TsPercent = 0.3
  df['playerBirthDate'] = df['playerBirthDate'].apply(lambda x: x.toordinal())
  df['gameDate'] = df['gameDate'].apply(lambda x: x.toordinal())
  Train = df.iloc[:int(len(df)*(1-TsPercent))]
  Test = df.iloc[int(len(df)*(1-TsPercent)):]
  yTrain = Train.flPoints
  yTest = Test.flPoints
  XTrain = Train.drop('flPoints',axis=1)
  XTest = Test.drop('flPoints',axis=1)
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

main()
