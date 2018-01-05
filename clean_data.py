import pandas as pd

#Note that this csv file does NOT contain statistics pertaining to goalies
df = pd.read_csv('hky_stats.csv')
df = df.drop(['gameId','playerBirthCity','playerBirthCountry','playerBirthStateProvince','playerFirstName','playerLastName','playerNationality'],axis=1)
df['flPoints'] = df.goals*3.0 + df.shots*0.1 + df.assists*2 + df.ppPoints + df.shPoints*2
print df.flPoints
print df.columns
