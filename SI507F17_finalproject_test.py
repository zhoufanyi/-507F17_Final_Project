import unittest
from SI507F17_finalproject import *
from bs4 import BeautifulSoup
from datetime import timedelta
import types

TEST_PLAYER_DICT = {'Player':'A', 'Games':12,'Minutes Played':'25:30','Field Goals Attempted':15,'Field Goals Made':8,'Field Goal Percentage':53.3,'Free Throws Attempted':5,'Free Throws Made':3,'Free Throw Percentage':60,'3-point Shots Attemped':3,'3-point Shots Made':1,'3-point Percentage':33.3,'Points Scored':22,'Offensive Rebounds':2,'Defensive Rebounds':5,'Total Rebounds':7,'Assists':3,'Steals':3,'Blocked Shots':1,'Turnovers':5,'Personal Fouls':2}

TEST_PLAYER_DICT_1 = {'Player':'A','Team':'Alpha', 'Games':12,'Minutes Played':timedelta(minutes=15,seconds=30),'Field Goals Attempted':9,'Field Goals Made':4.5,'Field Goal Percentage':50,'Free Throws Attempted':5,'Free Throws Made':3,'Free Throw Percentage':60,'3PT Shots Attemped':3,'3PT Shots Made':1,'3PT Percentage':33.3,'Points Scored':15,'Offensive Rebounds':2,'Defensive Rebounds':5,'Rebounds':7,'Assists':3,'Steals':3,'Blocked Shots':1,'Turnovers':5,'Personal Fouls':2}

TEST_PLAYER_DICT_2 = {'Player':'A','Team':'Beta', 'Games':5,'Minutes Played':timedelta(minutes=20,seconds=10),'Field Goals Attempted':15,'Field Goals Made':8,'Field Goal Percentage':53.3,'Free Throws Attempted':5,'Free Throws Made':3,'Free Throw Percentage':60,'3PT Shots Attemped':3,'3PT Shots Made':1,'3PT Percentage':33.3,'Points Scored':22,'Offensive Rebounds':2,'Defensive Rebounds':5,'Rebounds':7,'Assists':3,'Steals':3,'Blocked Shots':1,'Turnovers':5,'Personal Fouls':2}

TEST_PLAYER_LIST = [TEST_PLAYER_DICT_1,TEST_PLAYER_DICT_2]

TEST_TEAM_OFFENCE_DICT = {'Team':'B','Field Goals Made Per Game':20,'Field Goal Attempts Per Game':50,'Field Goal Percentage':40,'Three-Points Made Per Game':8,'Three-Point Attempts Per Game':24,'Three-Point Percentage':33.3,'Free Throws Made Per Game':15,'Free Throw Attempts Per Game':20,'Free Throw Percentage':75,'Offensive Rebounds Per Game':9,'Defensive Rebounds Per Game':10,'Total Rebounds Per Game':19,'Assists Per Game':18,'Turnovers Per Game':12,'Steals Per Game':5,'Blocked Shots Per Game':7,'Personal Fouls Per Game':14,'Points Per Game':90}

TEST_TEAM_DEFENCE_DICT = {'Team':'B','Field Goals Allowed Per Game':20,'Field Goal Attempts Allowed Per Game':50,'Field Goal Percentage Allowed':40,'Three-Points Allowed Per Game':8,'Three-Point Attempts Allowed Per Game':24,'Three-Point Percentage Allowed':33.3,'Free Throws Allowed Per Game':15,'Free Throw Attempts Allowed Per Game':20,'Free Throw Percentage Allowed':75,'Offensive Rebounds Allowed Per Game':9,'Defensive Rebounds Allowed Per Game':10,'Total Rebounds Allowed Per Game':19,'Assists Allowed Per Game':18,'Turnovers Forced Per Game':12,'Steals Forced Per Game':5,'Blocked Shots Allowed Per Game':7,'Personal Fouls Drawn Per Game':14,'Points Allowed Per Game':90}
TEST_TEAM = 'B'

class get_html_test(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_return(self):
        A = get_html(title = 'Base_Web')
        self.assertIsInstance(A,str)

class  get_player_stat_test(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_return(self):
        A = get_player_stat('Base_Web')
        self.assertIsInstance(A,list)

class get_team_stat_test(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_return(self):
        A = get_team_stat('Base_Web')
        self.assertIsInstance(A,list)   

class strip_multi_tag_test(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test(self):
        A = get_html(title = 'Base_Web')
        self.assertIsInstance(strip_multi_tag(A,'td'),types.GeneratorType)

class team_html_generator_test(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test(self):
        self.assertIsInstance(team_html_generator('Base_Web',''),types.GeneratorType)


class Player_test(unittest.TestCase):
    def setUp(self):
        self.test_player = Player(TEST_PLAYER_DICT,TEST_TEAM)
    def tearDown(self):
        self.test_player = None
    def test_Player_method(self):
        self.assertIsInstance(self.test_player.get_total_dict(),dict)
        self.assertIsInstance(self.test_player.get_average_dict(),dict)
        self.assertEqual(self.test_player.get_average_dict()['Points Scored'],22)
        self.assertEqual(self.test_player.get_total_dict()['Points Scored'],22*12)
        self.assertTrue(10 in self.test_player)
class team_test(unittest.TestCase):
    def setUp(self):
        self.team_obj = team('A')
    def tearDown(self):
        self.team_obj = None
    def test_get_method(self):
        self.assertEqual(self.team_obj.get_team_stat(), 'A')

class team_defence_test(unittest.TestCase):
    def setUp(self):
        self.team_defence_obj = team_defence.process_dict(TEST_TEAM_DEFENCE_DICT)
    def tearDown(self):
        self.team_defence = None
    def test_team_defence_method(self):
        self.assertIsInstance(self.team_defence_obj,team)
        self.assertIsInstance(self.team_defence_obj.team_stats, dict)
        self.assertEqual(self.team_defence_obj.team_stats['Field Goal Attempts'],50)
        self.assertTrue(100 in self.team_defence_obj )

class team_offence_test(unittest.TestCase):
    def setUp(self):
        self.team_offence_obj = team_offence.process_dict(TEST_TEAM_OFFENCE_DICT)
    def tearDown(self):
        self.team_offence = None
    def test_team_offence_method(self):
        self.assertIsInstance(self.team_offence_obj,team)
        self.assertIsInstance(self.team_offence_obj.team_stats, dict)
        self.assertEqual(self.team_offence_obj.team_stats['Field Goal Attempts'],50)
        self.assertFalse(100 in self.team_offence_obj)

class execute_and_return_test(unittest.TestCase):
    def setUP(self):
        pass
    def tearDown(self):
        pass
    def test(self):
        result = execute_and_return("""SELECT "Points","Assists", "Total Rebounds" FROM "Team Offence Stats" """)
        self.assertIsInstance(result,list)

class overall_stat_test(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test(self):
        self.assertIsInstance(overall_stat(TEST_PLAYER_LIST),dict)
        self.assertEqual(overall_stat(TEST_PLAYER_LIST)['Team'],'Alpha/Beta')
        self.assertEqual(overall_stat(TEST_PLAYER_LIST)['Points Scored'],37 )
        self.assertEqual(overall_stat(TEST_PLAYER_LIST)['Games'],17)



class overal_average_stat_test(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test(self):
        self.assertIsInstance(overall_average_stat(TEST_PLAYER_LIST),dict)
        self.assertEqual(overall_average_stat(TEST_PLAYER_LIST)['Team'],'Alpha/Beta')
        self.assertEqual(overall_average_stat(TEST_PLAYER_LIST)['Points Scored'],(15*12+22*5)/17)
        self.assertEqual(overall_average_stat(TEST_PLAYER_LIST)['Field Goal Percentage'],round((4.5*12+8*5)/(9*12+15*5)*100,1))

class player_all_plot_test(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test(self):
        self.assertIsInstance(player_all_plot(TEST_PLAYER_DICT_1),bytes)


class team_defence_plot_test(unittest.TestCase):
    def setUp(self):
        self.team_defence_obj = team_defence.process_dict(TEST_TEAM_DEFENCE_DICT)
    
    def tearDown(self):
        self.team_defence_obj = None
    
    def test(self):
        result = self.team_defence_obj.get_team_stat()
        self.assertIsInstance(team_defence_plot(result),bytes)

class team_offence_plot_test(unittest.TestCase):
    def setUp(self):
        self.team_offence_obj = team_offence.process_dict(TEST_TEAM_OFFENCE_DICT)
    
    def tearDown(self):
        self.team_offence_obj = None
    
    def test(self):
        result = self.team_offence_obj.get_team_stat()
        self.assertIsInstance(team_offence_plot(result),bytes)



if __name__ == '__main__':
    unittest.main(verbosity=2)