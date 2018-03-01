# NHL Fantasy League Predictor

## Motivation
* Get a better feel for using web-scraped data
* Complete a personal project (something that hasn't been prompted by Kaggle or
  a web based course)
* Gain experience using time series data
* Improve my ranking in my NHL Fantasy league

## Project Overview

### Objective
This project is intended to predict scores for my fantasey league given a set of features known before a game.

### Methods

### Python VS iPython
Jupyter Notebook using iPython is the standard for this sort of project, it's
easy to use and easy to follow. That being said all of my coding files for this project are in python rather than iPython. Why? I have limited access on one of the systems I am using to make this project and am unable to install jupyter note book or iPython. The amount of time I use that system is large enough where I felt it would be more beneficial to code in Python than iPython.

### Making the CSV
Currently I am scraping json data from the NHL statistics site with some
in-site filters applied,
[Link](http://www.nhl.com/stats/rest/skaters?isAggregate=false&reportType=basic&isGame=true&reportName=skatersummary&sort=[{%22property%22:%22points%22,%22direction%22:%22DESC%22},{%22property%22:%22goals%22,%22direction%22:%22DESC%22},{%22property%22:%22assists%22,%22direction%22:%22DESC%22}]&cayenneExp=gameDate%3E=%222017-10-04%22%20and%20gameDate%3C=%222018-01-02%22%20and%20gameTypeId=2).
This URL will have to be changed every time the model needs to be updated.

### Cleaning the data
Aside from some retyping there are two problems that can be found in the
feature columns:

1. NaN values(in draft related attributes)

2. "Future" data(in features like time on ice per game)

The NaN values in draft related attributes are caused by players who weren't
drafted. I used an average to fill in all the missing values in these cases.
This should allow me to keep these rows while keeping the influence of these
draft values at a minimum. 

The "Future" data is data that wouldn't be available at the time of a
prediction. Features like time on ice are a good example of this. Time on ice has an influence on fantasy league points(this can be seen from EDA done in
clean_data.csv) but is only known after the game. I'm going to make a model for
features like this during the modeling portion of this project and use that to
determine the values for these feature sets and for future instances.

### Exploratory Data Analysis
Originally I intended to do this in it's own file but it became too convenient
to clean the data and perform EDA at the same time. Most of the EDA showed
Gaussian relations between the feature and the label. It also showed that the
player age and player draft year features have very similar distributions with
an 18 year translation between the data sets. This makes sense after seeing the
PMF for age at draft was over 60% for 18.

### Modeling
Due to the nature of the data it makes the most sense to use one hot encoding
on many of the features the most important of which are player name, team, and opponent team. Encoding these causes the number of features to boom. I also suspect some of these features won't be important to the prediction. Support vector regression seems like a natural fit for this case. It should narrow the number of features to only those relevant and doesn't depend on statistical significance for determining the success of the model. Meaning the number of features I have shouldn't adversely effect the model.

I started by testing OLS on one of the "Future" data set models and back testing it with three splits. It performed poorly with all three splits yeilding coefficient of determinations that are on the 10 to the 12th order wich seems suspicious.

### Improvements
As this project hasn't yielded a model yet it's difficult for me to say what
improvements will impact it the most. I have considered using a different method
for filling NaN values for draft related data, maybe another model. I would also
like to use a SQL data base system, mainly so I can learn more about SQL
commands and how to use databases.

### Conclusion
More to come, I am actively working on this project. Hopefully within the next few
weeks I'll have enough of it finished to talk about it's accuracy.
