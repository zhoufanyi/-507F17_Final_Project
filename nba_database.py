from bs4 import BeautifulSoup
import requests
import os
from datetime import timedelta

PATH = os.getcwd()
#--------Caching System-----------#
def get_html(title, html = None, directory = None,update = False):
    if directory:
        path = os.path.join(PATH,directory)
    else:
        path =PATH
    if not os.path.exists(path):
        os.makedirs(directory)
    if update and os.path.exists(os.path.join(path ,title+'.html')):
        os.remove(os.path.join(path ,title+'.html'))
    try:
        page = open(os.path.join(path ,title+'.html'),'r',encoding = 'utf-8').read()
    except:
        page = requests.get(html).text
        f = open(os.path.join(path ,title+'.html'),'w',encoding='utf-8')
        f.write(page)
        f.close()
    return page

def strip_multi_tag(all_soup,tag):
    for item in all_soup.find_all(tag):
        yield item.text.strip()

def get_player_stat(html_page):
    players_list = []
    stats_name = []
    player_table_soup = BeautifulSoup(html_page,'html.parser').find('table',{'class':'table stats-table W(100%) Ta(start) Lh(2) Bdcl(c)'})
    for item in player_table_soup.find_all('th',{'class':'P(0px) Cur(p)'}):
        if 'title' in item.find('div').attrs.keys():
            stats_name.append(item.find('div')['title'])
        else:
            stats_name.append(item.find('div').text.strip())
    for player in player_table_soup.find_all('tr',{'class':'Px(cell-padding-x) Py(cell-padding-y) Bdb(row-border) Va(m) Ta(start)'}):
        stat = list(strip_multi_tag(player,'td'))
        stats_dict = dict(zip(stats_name,stat))
        players_list.append(stats_dict)
    return players_list





class player:
    def __init__(self,player_dict):
        self.Player = player_dict['Player']
        self.Games = int(player_dict['Games'])
        self.Minutes_Played = player_dict['Minutes Played']
        self.Field_Goals_Attempted = float(player_dict['Field Goals Attempted'])
        self.Field_Goals_Made = float(player_dict['Field Goals Made'])
        self.Field_Goal_Percentage = float(player_dict['Field Goal Percentage'])
        self.Free_Throws_Attempted = float(player_dict['Free Throws Attempted'])
        self.Free_Throws_Made = float(player_dict['Free Throws Made'])
        self.Free_Throw_Percentage = float(player_dict['Free Throw Percentage'])
        self.Three_point_Shots_Attemped = float(player_dict['3-point Shots Attemped'])
        self.Three_point_Shots_Made = float(player_dict['3-point Shots Made'])
        self.Three_point_Percentage = float(player_dict['3-point Percentage'])
        self.Points_Scored = float(player_dict['Points Scored'])
        self.Offensive_Rebounds = float(player_dict['Offensive Rebounds'])
        self.Defensive_Rebounds = float(player_dict['Defensive Rebounds'])
        self.Total_Rebounds = float(player_dict['Total Rebounds'])
        self.Assists = float(player_dict['Assists'])
        self.Steals = float(player_dict['Steals'])
        self.Blocked_Shots = float(player_dict['Blocked Shots'])
        self.Turnovers = float(player_dict['Turnovers'])
        self.Personal_Fouls = float(player_dict['Personal Fouls'])

    def get_average_dict(self):
        return {
                'Minutes Played':self.Minutes_Played,
                'Field Goals Attempted': self.Field_Goals_Attempted,
                'Field Goals Made': self.Field_Goals_Made,
                'Field Goal Percentage': self.Field_Goal_Percentage,
                'Free Throws Attempted': self.Free_Throws_Attempted,
                'Free Throws Made': self.Free_Throws_Made,
                'Free Throw Percentage': self.Free_Throw_Percentage,
                'Three Point Shots_Attemped': self.Three_point_Shots_Attemped,
                'Three Point Shots_Made': self.Three_point_Shots_Made,
                'Three Point Percentage': self.Three_point_Percentage,
                'Points Scored': self.Points_Scored,
                'Offensive Rebounds': self.Offensive_Rebounds,
                'Defensive Rebounds': self.Defensive_Rebounds,
                'Rebounds': self.Total_Rebounds,
                'Assists': self.Assists,
                'Steals': self.Steals,
                'Blocked Shots': self.Blocked_Shots,
                'Turnovers': self.Turnovers,
                'Personal Fouls': self.Personal_Fouls
            }

    def get_total_dict(self):
        avg_minutes = int(self.Minutes_Played.split(':')[0])
        avg_seconds = int(self.Minutes_Played.split(':')[1])
        total_time = (timedelta(minutes = avg_minutes, seconds = avg_seconds)*self.Games).total_seconds()
        seconds = int(total_time%60)
        minutes = int((total_time-seconds)/60)
        return{
                'Minutes Played':'{}:{}'.format(minutes,seconds),
                'Total Field Goals Attempted':int(self.Field_Goals_Attempted*self.Games),
                'Total Field Goals Made':int(self.Field_Goals_Made*self.Games),
                'Total Free Throws Attempted':int(self.Free_Throws_Attempted*self.Games),
                'Total Free Throws Made':int(self.Free_Throws_Made*self.Games),
                'Total Three Point Shots_Attemped':int(self.Three_point_Shots_Attemped*self.Games),
                'Total Three Point Shots_Made':int(self.Three_point_Shots_Made*self.Games),
                'Total Points Scored':int(self.Points_Scored*self.Games),
                'Total Offensive Rebounds':int(self.Offensive_Rebounds*self.Games),
                'Total Defensive Rebounds':int(self.Defensive_Rebounds*self.Games),
                'Total Rebounds':int(self.Total_Rebounds*self.Games),
                'Total Assists':int(self.Assists*self.Games),
                'Total Steals':int(self.Steals*self.Games),
                'Total Blocked Shots':int(self.Blocked_Shots*self.Games),
                'Total Turnovers':int(self.Turnovers*self.Games),
                'Total Personal Fouls':int(self.Personal_Fouls*self.Games)
            }

    def __str__(self):
        return '{} plays {} games this season with averge {} points, {} Rebounds and {} Assists'.format(self.Player,self.Games,self.Points_Scored, self.Total_Rebounds, self.Assists)

# class team:
#     self __init__(self,)
