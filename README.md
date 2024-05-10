# DSProject

Data Science Systems Final Project

Arjuna Bazaz - arjunabazaz@gmail.com

NBA stats database

Database Schema - 6 tables:
    Team
    Player
    Game
    Officials
    Game-Official
    Draft

Contains information on the 2021-2022 NBA season, has information on games played, players, officials, and the proceeding draft.

Data Sources: nba.sqlite and csv folder is from the nba database on Kaggle.
all_seasons.csv is also from Kaggle. draft information is generated from an api call
to the NBA stats website. nba.sqlite and csv folder exceed GitHub's file size limit, so a link is provided: https://www.kaggle.com/datasets/wyattowalsh/basketball

Data is loaded into nbadatabase.sqlite

ETL.py is the code for taking the data from the sources and creating nbadatabase.sqlite

sampleQueries.py is some examples of queries to that database for information on players and officials
