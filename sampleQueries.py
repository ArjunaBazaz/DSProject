import sqlite3
import pandas as pd
import requests

db_path = 'nbadatabase.sqlite'

con = sqlite3.connect(db_path)
cur = con.cursor()

#first query - how many free throw attempts does each official grant per game in 2022.
sql_query1 = '''
SELECT
    officials.first_name || ' ' || officials.last_name AS official_full_name,
    AVG((games.fta_home + games.fta_away)) AS avg_free_throw_attempts
FROM
    officials
JOIN
    `game-officials` ON `game-officials`.official_id = officials.official_id
JOIN
    games ON games.game_id = `game-officials`.game_id
GROUP BY
    officials.official_id, officials.first_name, officials.last_name;
'''
cur.execute(sql_query1)
rows = cur.fetchall()
df = pd.DataFrame(rows, columns=['official name', 'Average Free Throw Attempts per Game'])
print(df)

#second query - what was the impact of each rookie for their team this year. Measured by pts+reb+ast.
sql_query2 = '''
SELECT
    players.player_name,
    teams.full_name AS full_name,
    SUM(players.pts + players.reb + players.ast) AS total_score
FROM
    players
JOIN
    teams ON players.team_id = teams.team_id
JOIN
    draft ON players.player_id = draft.player_id
GROUP BY
    players.player_name, teams.full_name;
'''
cur.execute(sql_query2)
rows = cur.fetchall()
df = pd.DataFrame(rows, columns=['name', 'team', "sum total points, rebounds, and assists per game"])
print(df)

con.close()
