from bs4 import BeautifulSoup
import nba_database

test_player = {'Player': 'Dennis Schroder', 'Games': '20', 'Minutes Played': '32:07', 'Field Goals Attempted': '17.6', 'Field Goals Made': '8.1', 'Field Goal Percentage': '45.9', 'Free Throws Attempted': '3.4', 'Free Throws Made': '3.0', 'Free Throw Percentage': '88.2', '3-point Shots Attemped': '3.6', '3-point Shots Made': '1.2', '3-point Percentage': '33.3', 'Points Scored': '20.3', 'Offensive Rebounds': '0.8', 'Defensive Rebounds': '2.1', 'Total Rebounds': '2.8', 'Assists': '6.7', 'Steals': '1.2', 'Blocked Shots': '0.0', 'Turnovers': '3.0', 'Personal Fouls': '1.9'}
test_player_object = nba_database.player(test_player)
print(test_player_object.get_average_dict())
print(test_player_object.get_total_dict())