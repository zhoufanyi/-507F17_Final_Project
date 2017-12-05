from bs4 import BeautifulSoup
import nba_database

BASE_URL = 'https://sports.yahoo.com'
Base_Web = nba_database.get_html('Base_Web',BASE_URL+'/nba/stats/')
Team_Stats =nba_database.get_html('Team_Stats','https://sports.yahoo.com/nba/stats/team/?sortStatId=POINTS_PER_GAME&selectedTable=0',directory = 'Team_Stats',update = True)
Opposing_Team_Stats =nba_database.get_html('Opposing_Team_Stats','https://sports.yahoo.com/nba/stats/team/?sortStatId=POINTS_PER_GAME&selectedTable=1',directory = 'Team_Stats',update = True)
Base_Web_soup =BeautifulSoup(Base_Web,'html.parser')
for item in Base_Web_soup.find_all('li',{'class':"Lh(30px) Fz(14px)"}):
    information = item.find('a')
    link = BASE_URL+information['href']
    title = information.find('span').text.strip().replace(' ','_')
    nba_database.get_html(title, link,'Player_By_Team')

test = nba_database.get_html('Atlanta_Hawks' ,directory = 'Player_By_Team' )
#print(nba_database.get_player_stat(test))

