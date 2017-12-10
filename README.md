# -507F17_Final_Project

### Before use
1. make sure the python version is higher than 3.6
2. Create a virtual environment and install required modules described in **_requirement.txt_**.
3. Create a database and include database name, username and password in the **_config.py_** file. The **_config.py_** file shuold be put in the same directory where **_SI507F17_finalproject.py_** is.
4. The program starts up by **_python SI507F17_finalproject.py runserver_** in command line. Open any web browser and go to the localhost displayed in the command line.
5. Except for step 3, users are supposed to interact with the program through the web browser.

### Website Guide
   This website is designed to get latest NBA Player stats and Team stats. Before exploring the website, please read the following instructions.  
   
   You can search player's stats in **_player_** website. The search words are not case sensitive, but be aware of typying the full name of the player you are looking for.For example, 'Lebron James', 'lebron james' and 'leBron jAMes' are eligible key words. But 'james','James' and 'jAMEs' do not work here. 
   
   The search result contains two tables. One of them is the average stats this season, while the other is the total stats. Below the table, there are three histgrams about average points, average assists and average rebounds respectively. The black point in each histgram indicates where the player's stat locate. The is a pie chart decribing the player's distribution of points scored by three-point, field goals and free throw. 
   
   ![](https://github.com/zhoufanyi/-507F17_Final_Project/blob/master/example1.png)
   
   The tables have mulitiple rows if the player plays for different team this season. In this case, the last row of the table is the overall stats.
   
   ![](https://github.com/zhoufanyi/-507F17_Final_Project/blob/master/example2.png)
      
   The website **_team_** is desinged for getting the team stats this season. The keyword is the city where it locates, except for _'LA Clippers'_ and _'LA Lakers'_.  
   
   In the result, You will see two tables of offense and diffence stats of each teams. Below the table, there are two groups of histgrams about average points, average assists and average rebounds respectively at both offence and defence end. The black point in each histgram indicates where the team's stat locate. The is a pie chart decribing the teams's distribution of points scored by three-point, field goals and free throws.   
   ![](https://github.com/zhoufanyi/-507F17_Final_Project/blob/master/example3.png)  
   
   The database can be updated by clicking **_Update_** button. Because the data is scraped from website. It will take at most one minute. Please be patient and enjoy the database.

### Program Detail
#### class Player
This class is initialized with a string team name and a per game stat dictionary. Player class have two method which return a dictionary of player's per game stat and player's aggregate stat. All values in the returning dictionaries are modified to meet requirements of psql command. The str method returns a description of the player's average stat. 
```
Player A plays 12 games for Team X this season with averge 10 points, 3.2 Rebounds and 4.2 Assists.  
```
The contain method takes minutes as a float input and return True if the player plays more than the input miniutes in this team.  Suppose Player A playes 9 minutes per game in Team A.  
```
print(10 in Player A)
False
```

#### class team, team_defence and team_offence
The class team is initialized with a stat dictionary. The method get_team_stat returns self.team_stat which is a dictionary. Team_defence and team_offence are subclasses derived from team. These classes should be initialized through class method process_dict().
The str method of team_defence and team_offence gives a brief description of the team's stats.  
```
print(str(team_defence))    
 Team A lets opponent get 100 points this season with 39%  field goal percentage and 32% three-points percentage.  
print(str(team_offence))  
Team A scores 100 points this season with 39%  field goal percentage and 32% three-points percentage. 
```
The contain method of both class takes _point_ as a float input. The contain methond of team defence returns whether the team let the opponets score more than the _point_ on average. The one of team offence returns whether the team scores more than the _point_ on average.

### Caching System
The caching system consists of get_html(), team_html_generator(), strip_multi_tag(), get_player_stat() and get_team_stat().  
The whole system caches the desires websites from internet, get NBA players' stat and teams' stat with the help of beautifulsoup and returns dictionaries which will be used in initializing class Player and class team.  

### Database System
The database system consits of get_connection_and_cursor(), setup_database(), insert_player(), insert_team(), insert_update_team_table(), insert_update_player_table()  and execute_and_return(). This system helps connect to the database and create desired tables and colums. Then NBA stats dictionary will be insert into the database and updated to the latest version if needed with the help of psycopg2. The execute_and_return() gets the data from database for future use.

### Data Process System
The data process system is designed for handling the returning list of execute_and_return() when the list contains more than one dictionary. This happens when a player plays for more than one team in a season due to transactions. It will return a dictionary of average stats and aggregate stats in entire season.

### Plot System
The plot system contains player_all_plot(), team_offense_plot() and team_defense_plot(). These function takes dictionary input and draws histgram and pie chart with matplotlib. Then the figures are encoded in base64. The jinja template will decode them and regenerate figures in browser.

### Flask Part
There are three routes, which lead to index page, player search page annd team search page. Basically, user only needs to go to the '/' route and access to team by clicking team and to player by clicking player in index page. 
### Database Detail
There are four databases connected to the program.  
"Team Offence Stats"  
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
"Team Defence Stats"  
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

 "Player Stats Per Game"  
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
         PRIMARY KEY("Player","Team")  

"Player Stats Total"  
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
        PRIMARY KEY("Player","Team")  
