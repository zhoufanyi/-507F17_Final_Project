from bs4 import BeautifulSoup
import requests
import os
from datetime import timedelta
import psycopg2
import psycopg2.extras
from psycopg2 import sql
import sys
from config import *
from flask import Flask, request, render_template
import matplotlib.pyplot as plt
from io import BytesIO
import base64

BASE_URL = 'https://sports.yahoo.com'
PATH = os.getcwd()
##----------------------------------Caching System---------------------------##
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

def team_html_generator(Base,directory,update = False):
    Base_Web_soup =BeautifulSoup(Base,'html.parser')
    for item in Base_Web_soup.find_all('li',{'class':"Lh(30px) Fz(14px)"}):
            information = item.find('a')
            link = BASE_URL+information['href']
            team = information.find('span').text.strip()
            title = team.replace(' ','_')
            team_html = get_html(title,link,directory = directory,update = update)
            yield team, team_html

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

def get_team_stat(html_page):
    team_list = []
    stats_name = []
    team_table_soup = BeautifulSoup(html_page,'html.parser').find('table',{'class':'table graph-table W(100%) Ta(start) Bdcl(c) Mb(20px) Ov(h)'})
    for item in team_table_soup.find('thead').find_all('th'):
        stats_name.append(item['title'])
    for team in team_table_soup.find('tbody').find_all('tr'):
        stat = list(strip_multi_tag(team,'td'))
        stats_dict = dict(zip(stats_name,stat))
        team_list.append(stats_dict)
    return team_list

#---------------------------class player-----------------------------------#
class Player:
    def __init__(self,player_dict,team):
        self.Player = player_dict['Player']
        self.Team = team
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
        avg_minutes = int(self.Minutes_Played.split(':')[0])
        avg_seconds = int(self.Minutes_Played.split(':')[1])
        total_time = (timedelta(minutes = avg_minutes, seconds = avg_seconds)).total_seconds()
        hours = 0
        minutes = int(total_time/60)
        seconds = int(total_time-minutes*60)
        return {'Player': self.Player,
                'Team': self.Team,
                'Games':self.Games,
                'Minutes Played':'{'+'{}h {}m {}s'.format(hours,minutes,seconds)+'}',
                'Field Goals Attempted': self.Field_Goals_Attempted,
                'Field Goals Made': self.Field_Goals_Made,
                'Field Goal Percentage': self.Field_Goal_Percentage,
                'Free Throws Attempted': self.Free_Throws_Attempted,
                'Free Throws Made': self.Free_Throws_Made,
                'Free Throw Percentage': self.Free_Throw_Percentage,
                '3PT Shots Attemped': self.Three_point_Shots_Attemped,
                '3PT Shots Made': self.Three_point_Shots_Made,
                '3PT Percentage': self.Three_point_Percentage,
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
        hours = int(total_time/3600)
        minutes = int((total_time-hours*3600)/60)
        seconds = int(total_time-hours*3600-minutes*60)
        return{'Player': self.Player,
                'Team': self.Team,
                'Games':self.Games,        
                'Minutes Played':'{'+'{}h {}m {}s'.format(hours,minutes,seconds)+'}',
                'Field Goals Attempted':int(self.Field_Goals_Attempted*self.Games),
                'Field Goals Made':int(self.Field_Goals_Made*self.Games),
                'Free Throws Attempted':int(self.Free_Throws_Attempted*self.Games),
                'Free Throws Made':int(self.Free_Throws_Made*self.Games),
                '3PT Shots Attemped':int(self.Three_point_Shots_Attemped*self.Games),
                '3PT Shots Made':int(self.Three_point_Shots_Made*self.Games),
                'Points Scored':int(self.Points_Scored*self.Games),
                'Offensive Rebounds':int(self.Offensive_Rebounds*self.Games),
                'Defensive Rebounds':int(self.Defensive_Rebounds*self.Games),
                'Rebounds':int(self.Total_Rebounds*self.Games),
                'Assists':int(self.Assists*self.Games),
                'Steals':int(self.Steals*self.Games),
                'Blocked Shots':int(self.Blocked_Shots*self.Games),
                'Turnovers':int(self.Turnovers*self.Games),
                'Personal Fouls':int(self.Personal_Fouls*self.Games)
            }

    def __str__(self):
        return '{} plays {} games this season with averge {} points, {} Rebounds and {} Assists'.format(self.Player,self.Games,self.Points_Scored, self.Total_Rebounds, self.Assists)

    def __contains__(self,minutes):
        time_minutes = timedelta(minutes = minutes)
        avg_minutes = int(self.Minutes_Played.split(':')[0])
        avg_seconds = int(self.Minutes_Played.split(':')[1])
        total_time = timedelta(minutes = avg_minutes, seconds = avg_seconds)
        return total_time > time_minutes

##------------------------class team------------------------------##
class team:
    def __init__(self,stats_dict):
        self.team_stats = stats_dict

    def get_team_stat(self):
        return self.team_stats

class team_defence(team):
    def __init__(self,stats_dict):
        super().__init__(stats_dict)

    @classmethod
    def process_dict(cls,defence_dict):
        stats_dict ={'Team': defence_dict['Team'],
            'Field Goals Made': defence_dict['Field Goals Allowed Per Game'],
            'Field Goal Attempts': defence_dict['Field Goal Attempts Allowed Per Game'], 
            'Field Goal Percentage': defence_dict['Field Goal Percentage Allowed'],
            '3PT Made': defence_dict['Three-Points Allowed Per Game'],
            '3PT Attempts': defence_dict['Three-Point Attempts Allowed Per Game'],
            '3PT Percentage': defence_dict['Three-Point Percentage Allowed'],
            'Free Throws Made': defence_dict['Free Throws Allowed Per Game'],
            'Free Throw Attempts': defence_dict['Free Throw Attempts Allowed Per Game'],
            'Free Throw Percentage': defence_dict['Free Throw Percentage Allowed'],
            'Offensive Rebounds': defence_dict['Offensive Rebounds Allowed Per Game'],
            'Defensive Rebounds': defence_dict['Defensive Rebounds Allowed Per Game'],
            'Total Rebounds': defence_dict['Total Rebounds Allowed Per Game'],
            'Assists': defence_dict['Assists Allowed Per Game'],
            'Turnover': defence_dict['Turnovers Forced Per Game'],
            'Steal': defence_dict['Steals Forced Per Game'],
            'Blocked Shots': defence_dict['Blocked Shots Allowed Per Game'],
            'Personal Fous': defence_dict['Personal Fouls Drawn Per Game'],
            'Points': defence_dict['Points Allowed Per Game']
                }
        return cls(stats_dict)

    def __str__(self):
        return '{} lets opponent get {} points this season with {}% field goal percentage and {}% three-points percentage.'.format(self.team_stats['Team'],self.team_stats['Points'],self.team_stats['Field Goal Percentage'],self.team_stats['3PT Percentage'])

    def __contains__(self,point):
        return float(self.stats_dict['Points']) < point

class team_offence(team):
    def __init__(self,stats_dict):
        super().__init__(stats_dict)

    @classmethod
    def process_dict(cls,offence_dict):
        stats_dict ={'Team': offence_dict['Team'],
            'Field Goals Made': offence_dict['Field Goals Made Per Game'],
            'Field Goal Attempts': offence_dict['Field Goal Attempts Per Game'],
            'Field Goal Percentage': offence_dict['Field Goal Percentage'],
            '3PT Made': offence_dict['Three-Points Made Per Game'],
            '3PT Attempts': offence_dict['Three-Point Attempts Per Game'],
            '3PT Percentage': offence_dict['Three-Point Percentage'],
            'Free Throws Made': offence_dict['Free Throws Made Per Game'],
            'Free Throw Attempts': offence_dict['Free Throw Attempts Per Game'],
            'Free Throw Percentage': offence_dict['Free Throw Percentage'],
            'Offensive Rebounds': offence_dict['Offensive Rebounds Per Game'],
            'Defensive Rebounds': offence_dict['Defensive Rebounds Per Game'],
            'Total Rebounds': offence_dict['Total Rebounds Per Game'],
            'Assists': offence_dict['Assists Per Game'],
            'Turnover': offence_dict['Turnovers Per Game'],
            'Steal': offence_dict['Steals Per Game'],
            'Blocked Shots': offence_dict['Blocked Shots Per Game'],
            'Personal Fous': offence_dict['Personal Fouls Per Game'],
            'Points': offence_dict['Points Per Game']
                }
        return cls(stats_dict)

    def __str__(self):
        return '{} scores {} points this season with {}% field goal percentage and {}% three-points percentage.'.format(self.team_stats['Team'],self.team_stats['Points'],self.team_stats['Field Goal Percentage'],self.team_stats['3PT Percentage'])
    
    def __contains__(self,point):
        return float(self.stats_dict['Points']) > point


##------------------------Database-----------------------------------------##

def get_connection_and_cursor():
    global db_connection, db_cursor
    try:
        if not db_connection:
            if db_password != "":
                    db_connection = psycopg2.connect(dbname = db_name,user=db_user,password = db_password)
                    print("Success connecting to database")
            else:
                db_connection = psycopg2.connect(dbname = db_name,user=db_user)
    except:
        print("Unable to connect the database. Check the server and credentials.")
        sys.exit(1)
    if not db_cursor:
        db_cursor = db_connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)  

    return db_connection, db_cursor

def setup_database():
    db_cursor.execute(""" CREATE TABLE IF NOT EXISTS "Team Offence Stats"(
        "Team" VARCHAR(60) PRIMARY KEY,
        "Field Goal Attempts" REAL NOT NULL,
        "Field Goals Made" REAL NOT NULL,        
        "Field Goal Percentage" REAL NOT NULL,
        "Free Throw Attempts" REAL NOT NULL,
        "Free Throws Made" REAL NOT NULL,
        "Free Throw Percentage" REAL NOT NULL,
        "3PT Attempts" REAL NOT NULL,
        "3PT Made" REAL NOT NULL,      
        "3PT Percentage" REAL NOT NULL,
        "Offensive Rebounds" REAL NOT NULL,
        "Defensive Rebounds" REAL NOT NULL,
        "Total Rebounds" REAL NOT NULL,
        "Assists" REAL NOT NULL,
        "Turnover" REAL NOT NULL,
        "Steal" REAL NOT NULL,
        "Blocked Shots" REAL NOT NULL,
        "Personal Fous" REAL NOT NULL,
        "Points" REAL NOT NULL
        ) """)

    db_cursor.execute(""" CREATE TABLE IF NOT EXISTS "Team Defence Stats"(
        "Team" VARCHAR(60) PRIMARY KEY REFERENCES "Team Offence Stats"("Team"),
        "Field Goal Attempts" REAL NOT NULL,
        "Field Goals Made" REAL NOT NULL,        
        "Field Goal Percentage" REAL NOT NULL,
        "Free Throw Attempts" REAL NOT NULL,
        "Free Throws Made" REAL NOT NULL,
        "Free Throw Percentage" REAL NOT NULL,
        "3PT Attempts" REAL NOT NULL,
        "3PT Made" REAL NOT NULL,      
        "3PT Percentage" REAL NOT NULL,
        "Offensive Rebounds" REAL NOT NULL,
        "Defensive Rebounds" REAL NOT NULL,
        "Total Rebounds" REAL NOT NULL,
        "Assists" REAL NOT NULL,
        "Turnover" REAL NOT NULL,
        "Steal" REAL NOT NULL,
        "Blocked Shots" REAL NOT NULL,
        "Personal Fous" REAL NOT NULL,
        "Points" REAL NOT NULL
        ) """)

    db_cursor.execute("""CREATE TABLE IF NOT EXISTS "Player Stats Per Game"(
        "Player" VARCHAR(60),
        "Team" VARCHAR(60),
        "Games" INTEGER NOT NULL,
        "Minutes Played" INTERVAL MINUTE TO SECOND  NOT NULL,
        "Field Goals Attempted" REAL NOT NULL,
        "Field Goals Made" REAL NOT NULL,
        "Field Goal Percentage" REAL NOT  NULL,
        "Free Throws Attempted" REAL NOT NULL,
        "Free Throws Made" REAL NOT NULL,
        "Free Throw Percentage" REAL NOT NULL,
        "3PT Shots Attemped" REAL NOT NULL,
        "3PT Shots Made" REAL NOT NULL,
        "3PT Percentage" REAL NOT NULL,
        "Points Scored" REAL NOT NULL,
        "Offensive Rebounds" REAL NOT NULL,
        "Defensive Rebounds" REAL NOT NULL,
        "Rebounds" REAL NOT NULL,
        "Assists" REAL NOT NULL,
        "Steals" REAL NOT NULL,
        "Blocked Shots" REAL NOT NULL,
        "Turnovers" REAL NOT NULL,
        "Personal Fouls" REAL NOT NULL,
         PRIMARY KEY("Player","Team"))""")

    db_cursor.execute(""" CREATE TABLE IF NOT EXISTS "Player Stats Total"(
        "Player" VARCHAR(60),
        "Team" VARCHAR(60),
        "Games" INTEGER NOT NULL,
        "Minutes Played" INTERVAL MINUTE TO SECOND NOT NULL,
        "Field Goals Attempted" INTEGER NOT NULL,
        "Field Goals Made" INTEGER NOT NULL,
        "Free Throws Attempted" INTEGER NOT NULL,
        "Free Throws Made" INTEGER NOT NULL,
        "3PT Shots Attemped" INTEGER NOT NULL,
        "3PT Shots Made" INTEGER NOT NULL,
        "Points Scored" INTEGER NOT NULL,
        "Offensive Rebounds" INTEGER NOT NULL,
        "Defensive Rebounds" INTEGER NOT NULL,
        "Rebounds" INTEGER NOT NULL,
        "Assists" INTEGER NOT NULL,
        "Steals" INTEGER NOT NULL,
        "Blocked Shots" INTEGER NOT NULL,
        "Turnovers" INTEGER NOT NULL,
        "Personal Fouls" INTEGER NOT NULL,
        PRIMARY KEY("Player","Team")) """)

    db_connection.commit()

def insert_player(conn,cur,table,data_dict):
    column_names = data_dict.keys()
    query = sql.SQL('INSERT INTO{0}({1}) VALUES({2}) ON CONFLICT("Team","Player") DO UPDATE SET({1}) = ({2})').format(
        sql.SQL(table),
        sql.SQL(', ').join(map(sql.Identifier,
            column_names)),
        sql.SQL(', ').join(map(sql.Placeholder, column_names))
        )
    cur.execute(query,data_dict)

def insert_team(conn,cur,table,data_dict):
    column_names = data_dict.keys()
    query = sql.SQL('INSERT INTO{0}({1}) VALUES({2}) ON CONFLICT("Team") DO UPDATE SET({1}) = ({2})').format(
        sql.SQL(table),
        sql.SQL(', ').join(map(sql.Identifier,
            column_names)),
        sql.SQL(', ').join(map(sql.Placeholder, column_names))
        )
    query_string = query.as_string(conn)
    cur.execute(query_string,data_dict)

def insert_update_team_table(conn,cur,update = False):
    Team_Stats = get_html('Team_Stats','https://sports.yahoo.com/nba/stats/team/?sortStatId=POINTS_PER_GAME&selectedTable=0',directory = 'Team_Stats',update = update)
    Opposing_Team_Stats =get_html('Opposing_Team_Stats','https://sports.yahoo.com/nba/stats/team/?sortStatId=POINTS_PER_GAME&selectedTable=1',directory = 'Team_Stats',update = update)
    offence_list = get_team_stat(Team_Stats)
    defence_list = get_team_stat(Opposing_Team_Stats)
    offence_table = '"Team Offence Stats"'
    defence_table = '"Team Defence Stats"'
    for stat in offence_list:
        insert_team(conn,cur,offence_table,team_offence.process_dict(stat).get_team_stat())
    for stat in defence_list:
        team_defence.process_dict(stat).get_team_stat()
        insert_team(conn,cur,defence_table,team_defence.process_dict(stat).get_team_stat())
    conn.commit()

def insert_update_player_table(Base,directory,conn,cur,update =False):
    per_game_stat = '"Player Stats Per Game"'
    total_stat = '"Player Stats Total"'
    for item in team_html_generator(Base,directory,update = update):
        team, team_html = item
        player_list = get_player_stat(team_html)
        for player in player_list:
            player_obj = Player(player,team)
            insert_player(conn,cur,per_game_stat,player_obj.get_average_dict())
            insert_player(conn,cur,total_stat,player_obj.get_total_dict())
    conn.commit()

def execute_and_return(query):
    db_cursor.execute(query)
    results = db_cursor.fetchall()
    if len(results) != 0:
        return results
    else:
        return False

def overall_stat(stat_list):
    overall_stat_dict = {}
    overall_stat_dict['Player'] = stat_list[0]['Player']
    overall_stat_dict['Team'] = stat_list[0]['Team']
    overall_stat_dict['Games'] = int(stat_list[0]['Games'])
    overall_stat_dict['Minutes Played'] = stat_list[0]['Minutes Played']
    overall_stat_dict['Field Goals Attempted'] = float(stat_list[0]['Field Goals Attempted'])
    overall_stat_dict['Field Goals Made'] = float(stat_list[0]['Field Goals Made'])
    overall_stat_dict['Free Throws Attempted'] = float(stat_list[0]['Free Throws Attempted'])
    overall_stat_dict['Free Throws Made'] = float(stat_list[0]['Free Throws Made'])
    overall_stat_dict['3PT Shots Attemped'] = float(stat_list[0]['3PT Shots Attemped'])
    overall_stat_dict['3PT Shots Made'] = float(stat_list[0]['3PT Shots Made'])
    overall_stat_dict['Points Scored'] = float(stat_list[0]['Points Scored'])
    overall_stat_dict['Offensive Rebounds'] = float(stat_list[0]['Offensive Rebounds'])
    overall_stat_dict['Defensive Rebounds'] = float(stat_list[0]['Defensive Rebounds'])
    overall_stat_dict['Rebounds'] = float(stat_list[0]['Rebounds'])
    overall_stat_dict['Assists'] = float(stat_list[0]['Assists'])
    overall_stat_dict['Steals'] = float(stat_list[0]['Steals'])
    overall_stat_dict['Blocked Shots'] = float(stat_list[0]['Blocked Shots'])
    overall_stat_dict['Turnovers'] = float(stat_list[0]['Turnovers'])
    overall_stat_dict['Personal Fouls'] = float(stat_list[0]['Personal Fouls'])
    for item in stat_list[1:]:
        overall_stat_dict['Team'] += '/'+item['Team']
        overall_stat_dict['Games'] += int(item['Games'])
        overall_stat_dict['Minutes Played'] += item['Minutes Played']
        overall_stat_dict['Field Goals Attempted'] += float(item['Field Goals Attempted'])
        overall_stat_dict['Field Goals Made'] += float(item['Field Goals Made'])
        overall_stat_dict['Free Throws Attempted'] += float(item['Free Throws Attempted'])
        overall_stat_dict['Free Throws Made'] += float(item['Free Throws Made'])
        overall_stat_dict['3PT Shots Attemped'] += float(item['3PT Shots Attemped'])
        overall_stat_dict['3PT Shots Made'] += float(item['3PT Shots Made'])
        overall_stat_dict['Points Scored'] += float(item['Points Scored'])
        overall_stat_dict['Offensive Rebounds'] += float(item['Offensive Rebounds'])
        overall_stat_dict['Defensive Rebounds'] += float(item['Defensive Rebounds'])
        overall_stat_dict['Rebounds'] += float(item['Rebounds'])
        overall_stat_dict['Assists'] += float(item['Assists'])
        overall_stat_dict['Steals'] += float(item['Steals'])
        overall_stat_dict['Blocked Shots'] += float(item['Blocked Shots'])
        overall_stat_dict['Turnovers'] += float(item['Turnovers'])
        overall_stat_dict['Personal Fouls'] += float(item['Personal Fouls'])        
    total_seconds = overall_stat_dict['Minutes Played'].total_seconds()
    minutes = str(int(total_seconds/60))
    seconds = str(int(total_seconds%60))
    overall_stat_dict['Minutes Played'] = '{} : {}'.format(minutes,seconds)
    return overall_stat_dict

def overall_average_stat(stat_list):
    overall_average_stat_dict = {} 
    overall_average_stat_dict['Player'] =stat_list[0]['Player']
    overall_average_stat_dict['Team'] = stat_list[0]['Team']
    overall_average_stat_dict['Games'] = int(stat_list[0]['Games'])
    overall_average_stat_dict['Minutes Played'] = stat_list[0]['Minutes Played']*float(stat_list[0]['Games'])
    overall_average_stat_dict['Field Goals Attempted'] = float(stat_list[0]['Field Goals Attempted'])*float(stat_list[0]['Games'])
    overall_average_stat_dict['Field Goals Made'] = float(stat_list[0]['Field Goals Made'])*float(stat_list[0]['Games'])
    overall_average_stat_dict['Field Goal Percentage'] = 0
    overall_average_stat_dict['Free Throws Attempted'] = float(stat_list[0]['Free Throws Attempted'])*float(stat_list[0]['Games'])
    overall_average_stat_dict['Free Throws Made'] = float(stat_list[0]['Free Throws Made'])*float(stat_list[0]['Games'])
    overall_average_stat_dict['Free Throw Percentage'] = 0
    overall_average_stat_dict['3PT Shots Attemped'] = float(stat_list[0]['3PT Shots Attemped'])*float(stat_list[0]['Games'])
    overall_average_stat_dict['3PT Shots Made'] = float(stat_list[0]['3PT Shots Made'])*float(stat_list[0]['Games'])
    overall_average_stat_dict['3PT Percentage'] = 0
    overall_average_stat_dict['Points Scored'] = float(stat_list[0]['Points Scored'])*float(stat_list[0]['Games'])
    overall_average_stat_dict['Offensive Rebounds'] = float(stat_list[0]['Offensive Rebounds'])*float(stat_list[0]['Games'])
    overall_average_stat_dict['Defensive Rebounds'] = float(stat_list[0]['Defensive Rebounds'])*float(stat_list[0]['Games'])
    overall_average_stat_dict['Rebounds'] = float(stat_list[0]['Rebounds'])*float(stat_list[0]['Games'])
    overall_average_stat_dict['Assists'] = float(stat_list[0]['Assists'])*float(stat_list[0]['Games'])
    overall_average_stat_dict['Steals'] = float(stat_list[0]['Steals'])*float(stat_list[0]['Games'])
    overall_average_stat_dict['Blocked Shots'] = float(stat_list[0]['Blocked Shots'])*float(stat_list[0]['Games'])
    overall_average_stat_dict['Turnovers'] = float(stat_list[0]['Turnovers'])*float(stat_list[0]['Games'])
    overall_average_stat_dict['Personal Fouls'] = float(stat_list[0]['Personal Fouls'])*float(stat_list[0]['Games'])
    for item in stat_list[1:]:
        overall_average_stat_dict['Team'] += '/'+item['Team']
        overall_average_stat_dict['Games'] += int(item['Games'])
        overall_average_stat_dict['Minutes Played'] += item['Minutes Played']*float(item['Games'])
        overall_average_stat_dict['Field Goals Attempted'] += float(item['Games'])*float(item['Field Goals Attempted'])
        overall_average_stat_dict['Field Goals Made'] += float(item['Games'])*float(item['Field Goals Made'])
        overall_average_stat_dict['Free Throws Attempted'] += float(item['Games'])*float(item['Free Throws Attempted'])
        overall_average_stat_dict['Free Throws Made'] += float(item['Games'])*float(item['Free Throws Made'])
        overall_average_stat_dict['3PT Shots Attemped'] += float(item['Games'])*float(item['3PT Shots Attemped'])
        overall_average_stat_dict['3PT Shots Made'] += float(item['Games'])*float(item['3PT Shots Made'])
        overall_average_stat_dict['Points Scored'] += float(item['Games'])*float(item['Points Scored'])
        overall_average_stat_dict['Offensive Rebounds'] += float(item['Games'])*float(item['Offensive Rebounds'])
        overall_average_stat_dict['Defensive Rebounds'] += float(item['Games'])*float(item['Defensive Rebounds'])
        overall_average_stat_dict['Rebounds'] += float(item['Games'])*float(item['Rebounds'])
        overall_average_stat_dict['Assists'] += float(item['Games'])*float(item['Assists'])
        overall_average_stat_dict['Steals'] += float(item['Games'])*float(item['Steals'])
        overall_average_stat_dict['Blocked Shots'] += float(item['Games'])*float(item['Blocked Shots'])
        overall_average_stat_dict['Turnovers'] += float(item['Games'])*float(item['Turnovers'])
        overall_average_stat_dict['Personal Fouls'] += float(item['Games'])*float(item['Personal Fouls'])       
    overall_average_stat_dict['Field Goal Percentage'] =round(float(overall_average_stat_dict['Field Goals Made']/overall_average_stat_dict['Field Goals Attempted'] )* 100,1) 
    overall_average_stat_dict['Free Throw Percentage'] = round(float(overall_average_stat_dict['Free Throws Made']/overall_average_stat_dict['Free Throws Attempted'] )* 100,1)
    overall_average_stat_dict['3PT Percentage'] =round(float(overall_average_stat_dict['3PT Shots Made']/overall_average_stat_dict['3PT Shots Attemped'] )* 100,1)
    overall_average_stat_dict['Minutes Played'] = overall_average_stat_dict['Minutes Played'] /float(overall_average_stat_dict['Games'])
    for k in overall_average_stat_dict.keys():
        if k not in ['Player','Team','Games','Minutes Played','Field Goal Percentage','Free Throw Percentage','3PT Percentage']:
          overall_average_stat_dict[k] = overall_average_stat_dict[k]/overall_average_stat_dict['Games']
    total_seconds = (overall_average_stat_dict['Minutes Played']).total_seconds()
    minutes = str(int(total_seconds/60))
    seconds = str(int(total_seconds%60))
    overall_average_stat_dict['Minutes Played'] = '{} : {}'.format(minutes,seconds)
    return overall_average_stat_dict

def player_all_plot(result):
    query_result = execute_and_return("""SELECT "Points Scored","Assists", "Rebounds" FROM "Player Stats Per Game" """)
    Points = [item['Points Scored'] for item in query_result]
    Assists = [item['Assists'] for item in query_result]
    Rebounds = [item['Rebounds'] for item in query_result]
    plt.figure(figsize=(10,2.5))
    plt.subplot(1,4,1)
    plt.hist(Points,bins = 100, density = True,color = 'red')
    plt.plot(result['Points Scored'],0,'o',color = 'black')
    plt.title('Points Scored')
    plt.subplot(1,4 ,2)
    plt.hist(Assists,bins = 100, density = True,color = 'green')
    plt.title('Assists') 
    plt.plot(result['Assists'],0,'o',color = 'black')
    plt.subplot(1,4,3)
    plt.hist(Rebounds,bins = 100, density = True,color = 'yellow')
    plt.title('Rebounds')
    plt.plot(result['Rebounds'],0,'o',color = 'black')
    plt.subplot(1,4,4)
    label='Field Goal','3PT','Free Throw'
    size = (result['Field Goals Made']*2,result['3PT Shots Made']*3,result['Free Throws Made'])
    max_index = size.index(max(size))
    explode = [0,0,0]
    explode[max_index] = 0.1
    plt.pie(size,explode = explode, labels = label)
    plt.title('Points Distribution')
    figfile =BytesIO()
    plt.savefig(figfile,format = 'png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    return figdata_png

def team_offense_plot(result):
    query_result = execute_and_return("""SELECT "Points","Assists", "Total Rebounds" FROM "Team Offence Stats" """)
    Points = [item['Points'] for item in query_result]
    Assists = [item['Assists'] for item in query_result]
    Rebounds = [item['Total Rebounds'] for item in query_result]
    plt.figure(figsize=(10,2.5))
    plt.subplot(1,4,1)
    plt.hist(Points,bins = 10, density = True,color = 'red')
    plt.plot(result['Points'],0,'o',color = 'black')
    plt.title('Points Scored')
    plt.subplot(1,4 ,2)
    plt.hist(Assists,bins = 10, density = True,color = 'green')
    plt.title('Assists') 
    plt.plot(result['Assists'],0,'o',color = 'black')
    plt.subplot(1,4,3)
    plt.hist(Rebounds,bins = 10, density = True,color = 'yellow')
    plt.title('Rebounds')
    plt.plot(result['Total Rebounds'],0,'o',color = 'black')
    plt.subplot(1,4,4)
    label='Field Goals','Free Throws','3PT'
    size = (result['Field Goals Made']*2,result['3PT Made']*3,result['Free Throws Made'])
    max_index = size.index(max(size))
    explode = [0,0,0]
    explode[max_index] = 0.1
    plt.pie(size,explode = explode, labels = label)
    plt.title('Points Distribution')
    figfile =BytesIO()
    plt.savefig(figfile,format = 'png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    return figdata_png

def team_defense_plot(result):
    query_result = execute_and_return("""SELECT "Points","Assists", "Total Rebounds" FROM "Team Defence Stats" """)
    Points = [item['Points'] for item in query_result]
    Assists = [item['Assists'] for item in query_result]
    Rebounds = [item['Total Rebounds'] for item in query_result]
    plt.figure(figsize=(7.5,2.5))
    plt.subplot(1,3,1)
    plt.hist(Points,bins = 10, density = True,color = 'red')
    plt.plot(result['Points'],0,'o',color = 'black')
    plt.title('Points Scored')
    plt.subplot(1,3,2)
    plt.hist(Assists,bins = 10, density = True,color = 'green')
    plt.title('Assists') 
    plt.plot(result['Assists'],0,'o',color = 'black')
    plt.subplot(1,3,3)
    plt.hist(Rebounds,bins = 10, density = True,color = 'yellow')
    plt.title('Rebounds')
    plt.plot(result['Total Rebounds'],0,'o',color = 'black')
    figfile =BytesIO()
    plt.savefig(figfile,format = 'png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    return figdata_png

#---------------------------------#
test_dict = {'Player':'A B', 'Games':12,'Minutes Played':'25:30','Field Goals Attempted':15,'Field Goals Made':8,'Field Goal Percentage':53.3,'Free Throws Attempted':5,'Free Throws Made':3,'Free Throw Percentage':60,'3-point Shots Attemped':3,'3-point Shots Made':1,'3-point Percentage':33.3,'Points Scored':22,'Offensive Rebounds':2,'Defensive Rebounds':5,'Total Rebounds':7,'Assists':3,'Steals':3,'Blocked Shots':1,'Turnovers':5,'Personal Fouls':2}
test_player_1 = Player(test_dict,'Miami Heat')
test_player_2 = Player(test_dict,'Boston Celtics')
test_player_1_average = test_player_1.get_average_dict()
test_player_1_total = test_player_1.get_total_dict()
test_player_2_average = test_player_1.get_average_dict()
test_player_2_total = test_player_2.get_total_dict()
##----------------------------------##
db_connection, db_cursor = None, None
db_connection, db_cursor = get_connection_and_cursor()
Base_Web = get_html('Base_Web',BASE_URL+'/nba/stats/')

app =Flask(__name__)

@app.route('/')
def index():
    update = request.args.get('update')
    if update:
        insert_update_team_table(db_connection, db_cursor,update = True)
        insert_update_player_table(Base_Web,directory='Player_By_Team',conn = db_connection,cur = db_cursor,update = True)
        result = True
    else:
        result = False
    return render_template('index.html',result = result)


@app.route('/player')
def player_site():
    results1 = []
    results2 = []
    respones = {}
    search = request.args.get('name')
    if search:
        query1 = sql.SQL('SELECT * FROM "Player Stats Per Game" WHERE "Player" ILIKE {0} ').format(sql.SQL('\''+search+'\''))
        query2 = sql.SQL('SELECT * FROM "Player Stats Total" WHERE "Player" ILIKE {0} ').format(sql.SQL('\''+search+'\''))
        results1 = execute_and_return(query1)
        if not results1:
            results1 = False
        else:
            if len(results1) > 1:
                respones['results3'] = overall_average_stat(results1)
                respones['all_plot'] = player_all_plot(respones['results3']).decode('utf-8')
            else:
                respones['all_plot'] = player_all_plot(results1[0]).decode('utf-8')
            for item in results1:
                total_seconds = item['Minutes Played'].total_seconds()
                minutes = str(int(total_seconds/60))
                seconds = str(int(total_seconds%60))
                item['Minutes Played'] = '{} : {}'.format(minutes,seconds)

        results2 = execute_and_return(query2)
        if not results2:
            results2 = False
        else:
            if len(results2) > 1:     
                respones['results4'] = overall_stat(results2)  
            for item in results2:
                total_seconds = item['Minutes Played'].total_seconds()
                minutes = str(int(total_seconds/60))
                seconds = str(int(total_seconds%60))
                item['Minutes Played'] = '{} : {}'.format(minutes,seconds)
    return render_template('player.html',search = search, results1 = results1,results2 = results2,respones = respones)


@app.route('/team')
def team_site():
    search = request.args.get('team')
    results1 = []
    results2 = []
    respones = {}
    if search:
        query1 = sql.SQL('SELECT * FROM "Team Offence Stats" WHERE "Team" ILIKE {0}').format(sql.SQL('\''+search+'\''))
        query2 = sql.SQL('SELECT * FROM "Team Defence Stats" WHERE "Team" ILIKE {0}').format(sql.SQL('\''+search+'\''))
        results1 = execute_and_return(query1)
        if not results1:
            results1 = False
        else:
            respones['offence_plot'] = team_offense_plot(results1[0]).decode('utf-8')

        results2 = execute_and_return(query2)
        if not results1:
            results2 = False
        else:
            respones['defence_plot'] = team_defense_plot(results2[0]).decode('utf-8')

    return render_template('team.html',search = search, results1 = results1,results2 = results2,respones = respones)


if __name__ == '__main__':
    setup_database()
    insert_update_team_table(db_connection, db_cursor)
    insert_update_player_table(Base_Web,directory='Player_By_Team',conn = db_connection,cur = db_cursor)
    app.run(use_reloader=True, debug = True)
