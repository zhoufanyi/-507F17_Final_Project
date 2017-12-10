# -507F17_Final_Project

### Before use
1. Create a virtual environment and install required modules described in **_requirement.txt_**.
2. Create a database and include database name, username and password in the **_config.py_** file. The **_config.py_** file shuold be put in the same directory where **_SI507F17_finalproject.py_** is.
3. The program starts up by **_python SI507F17_finalproject.py runserver_** in command line. Open any web browser and go to the localhost displayed in the command line.
4. Except for step 3, users are supposed to interact with the program through the web browser.

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
This class is initialized with a str and a dictionary. Player class have two method which return a dictionary of player's per game stat and player's aggregate stat. All values in the returning dictionaries are modified to meet requirements of psql command. The str method returns a description of the player's average stat.  
> _Player A_ plays _12_ games for _Team X_ this season with averge _10_ points, _3.2_ Rebounds and _4.2_ Assists.
