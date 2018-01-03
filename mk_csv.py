#Intended to write a CSV file containing the statistics of current NHL players

import pandas as pd
import requests
import json
import csv

HkDic = requests.get('http://www.nhl.com/stats/rest/skaters?isAggregate=false&reportType=basic&isGame=true&reportName=skatersummary&sort=[{%22property%22:%22points%22,%22direction%22:%22DESC%22},{%22property%22:%22goals%22,%22direction%22:%22DESC%22},{%22property%22:%22assists%22,%22direction%22:%22DESC%22}]&cayenneExp=gameDate%3E=%222017-10-04%22%20and%20gameDate%3C=%222018-01-02%22%20and%20gameTypeId=2')
HkDic = json.loads(HkDic.text)
HkDic = HkDic['data']
print type(HkDic[0])
df = pd.DataFrame(HkDic[0],index=[0])
for i in range(1,5):
  df.append(pd.DataFrame(HkDic[i],index[i])
print df
#with open('hky_stats.csv', 'wb') as f:
 #   for Dic in HkDic:
  #    w = csv.DictWriter(f, Dic.keys())
      #w.writeheader()
      #w.writerow(Dic)
