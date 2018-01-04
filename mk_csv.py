#Intended to write a CSV file containing the statistics of current NHL players
#the URL might have to be renewed I'm unsure if data is added to it or a new
#one is made when new data becomes available
import pandas as pd
import requests
import json

#visit this site to get a new URL if needed, http://www.nhl.com/stats/player?reportType=game&dateFrom=2017-10-04&dateTo=2018-01-02&gameType=2&filter=gamesPlayed,gte,1&sort=points,goals,assists

#Imports data from website then reduces it to a dictionary of dictionaries containing the data
HkDic = requests.get('http://www.nhl.com/stats/rest/skaters?isAggregate=false&reportType=basic&isGame=true&reportName=skatersummary&sort=[{%22property%22:%22points%22,%22direction%22:%22DESC%22},{%22property%22:%22goals%22,%22direction%22:%22DESC%22},{%22property%22:%22assists%22,%22direction%22:%22DESC%22}]&cayenneExp=gameDate%3E=%222017-10-04%22%20and%20gameDate%3C=%222018-01-02%22%20and%20gameTypeId=2')
HkDic = json.loads(HkDic.text)
HkDic = HkDic['data']

#Converts one of the dictionaries to a data frame then does the same for the rest and appends them
#I tried in place methodes for appending the data like .loc but this seems to be fastest
df = pd.DataFrame(HkDic[0],index=[0])
for i in range(1,len(HkDic)):
  df = df.append(pd.DataFrame(HkDic[i],index=[i]))
df.to_csv('hky_stats.csv',encoding='utf-8')
