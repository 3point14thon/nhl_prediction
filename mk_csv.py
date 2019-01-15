import pandas as pd
import requests
import json


def main(url):
  '''
  Intended to write a CSV file containing the statistics of current NHL players

  Args:
    url: the url to request from

  Returns: None
  '''
  hkdic = requests.get(url)
  df = pd.DataFrame.from_dict(hkdic.json()['data'])
  df.to_csv('hky_stats.csv',encoding='utf-8')


if __name__ == '__main__':
  #url may need to be updated for most recent statistics
  main('http://www.nhl.com/stats/rest/skaters?isAggregate=false&reportType=basic&isGame=true&reportName=skatersummary&sort=[{%22property%22:%22points%22,%22direction%22:%22DESC%22},{%22property%22:%22goals%22,%22direction%22:%22DESC%22},{%22property%22:%22assists%22,%22direction%22:%22DESC%22}]&cayenneExp=gameDate%3E=%222017-10-04%22%20and%20gameDate%3C=%222018-01-02%22%20and%20gameTypeId=2')
