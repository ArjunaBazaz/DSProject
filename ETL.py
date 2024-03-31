import sqlite3
import pandas as pd
import requests
    
#team table
df = pd.read_csv('csv/team.csv')
df = df.drop(columns=["nickname"])
df = df.rename(columns={'id': 'team_id'})
db_path = 'nbadatabase.sqlite'
table_name = 'teams'
conn = sqlite3.connect(db_path)
df.to_sql(table_name, conn, if_exists='replace', index=False)
conn.close()

#player table
df2 = pd.read_csv('all_seasons.csv')
df2 = df2[df2['season'] == "2021-22"]
db_path = 'nbadatabase.sqlite'
table_name = 'players'
con = sqlite3.connect(db_path)
team_id = []
for index, row in df2.iterrows():
    team_abbreviation = row['team_abbreviation']
    cur = con.cursor()
    cur.execute("SELECT team_id FROM teams WHERE abbreviation = ?", (team_abbreviation,))
    result = cur.fetchone()
    if result:
        team_id.append(result[0])
    else:
        print(f"No team found for abbreviation {team_abbreviation}")
        df2 = df2.drop(index)
df2['team_id'] = team_id
df2 = df2.drop(columns=["season", "team_abbreviation"])
df2.to_sql(table_name, con, if_exists='replace', index=False)
con.close()

#game table
con = sqlite3.connect("nba.sqlite")
con2 = sqlite3.connect("nbadatabase.sqlite")
table_name = 'games'
cur = con.cursor()
cur.execute('SELECT * FROM game WHERE season_id = 12021')
rows = cur.fetchall()
columns = [col[0] for col in cur.description]
df3 = pd.DataFrame(rows, columns=columns)
df3 = df3.drop(columns=["video_available_away", "video_available_home", "season_id", "team_name_home", "team_name_away", "team_abbreviation_home", "team_abbreviation_away"])
df3.to_sql(table_name, con2, if_exists='replace', index=False)
con.close()

#officials table
con = sqlite3.connect("nba.sqlite")
con2 = sqlite3.connect("nbadatabase.sqlite")
table_name = 'officials'
cur = con.cursor()
cur.execute('SELECT * FROM officials')
rows = cur.fetchall()
columns = [col[0] for col in cur.description]
df4 = pd.DataFrame(rows, columns=columns)
df4 = df4.drop(columns=["jersey_num", "game_id"])
df4 = df4.drop_duplicates()
df4.to_sql(table_name, con2, if_exists='replace', index=False)
con.close()
con2.close()

#official-game table
con = sqlite3.connect("nba.sqlite")
con2 = sqlite3.connect("nbadatabase.sqlite")
table_name = 'game-officials'
cur = con.cursor()
cur.execute('SELECT * FROM officials')
rows = cur.fetchall()
columns = [col[0] for col in cur.description]
df5 = pd.DataFrame(rows, columns=columns)
df5 = df5.drop(columns=["jersey_num", "first_name", "last_name"])
df5 = df5.drop_duplicates()
df5.to_sql(table_name, con2, if_exists='replace', index=False)
con.close()

#draft table
url = 'https://stats.nba.com/stats/drafthistory'
headers= {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
          'Referer': 'https://www.nba.com/'}
payload = {
    'Season': '2021'
    }
try:
    jsonData = requests.get(url, headers=headers, params=payload).json()
except():
    print("api call failed")
rows = jsonData['resultSets'][0]['rowSet']
columns = jsonData['resultSets'][0]['headers']
df6 = pd.DataFrame(rows, columns=columns)
df6 = df6.drop(columns=["SEASON", "PLAYER_PROFILE_FLAG", "TEAM_CITY", "TEAM_ABBREVIATION", "PERSON_ID"])
player_ids = []
con = sqlite3.connect("nbadatabase.sqlite")
for index, row in df6.iterrows():
    player_name = row['PLAYER_NAME']
    cur = con.cursor()
    cur.execute("SELECT player_id FROM players WHERE player_name = ?", (player_name,))
    result = cur.fetchone()
    if result:
        player_ids.append(result[0])
    else:
        print(f"{player_name} did not play in the NBA the year after getting drafted.")
        df6 = df6.drop(index)
df6['player_id'] = player_ids
table_name = 'draft'
df6.to_sql(table_name, con, if_exists='replace', index=False)
con.close()