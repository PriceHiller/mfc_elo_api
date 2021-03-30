#This program calculates the ELO Rating of a team, based on the score between 
#them in a Best of 5 map set, using an Elo formula created by Tucker and 
#Montresor for the NA Mordhau Fight Club

#Thanks for the help chaq!


# maybe make a big super class, call it uhhh
# class Elobot and then it has a Team subclass and
# an Elo subclass?? Then have it instantiate as 
# many teams as requested in main(), and have it 
# feed info into the elo subclass calculate method
# using *args maybe?

print('Launching MFC Elobot...')

class Team:

    def __init__(self, name, rating, mapsWon):
        self.name = name
        self.rating = rating
        self.mapsWon = mapsWon

    def createTeam():
        name = input('Team name: ')
        rating = int(input(f'{name}\'s rating: '))
        mapsWon = int(input('Maps won: '))
        return Team(name, rating, mapsWon)




class Elo:

    def __init__(self):
        pass

    def calculate():
        newRating1 = round(team_1.rating + (150 * (scoreList[0] - expScoreList[0])) + baseValList[0])
        team2NewRating = round(team_2.rating + (150 * (scoreList[1] - expScoreList[1])) + baseValList[1])

        eloDiff1 = team1NewRating - team_1.rating
        eloDiff2 = team2NewRating - team_2.rating
        pass






def matchScore():
    line(50)
    print('Calculating actual match scores...')

    score1 = team_1.mapsWon / (team_1.mapsWon + team_2.mapsWon)
    print('score1:', score1)
    score2 = team_2.mapsWon / (team_2.mapsWon + team_1.mapsWon)
    print('score2:', score2)

    li = []
    li.append(score1)
    li.append(score2)
    return li

def baseline():
    #this is the actual math for calculating baselineValue, it gives same results as baseline() assuming a bo5 series
    #myVariable = 25 * ((team_1.mapsWon - team_2.mapsWon) / abs(team_1.mapsWon - team_2.mapsWon))
    print('Calculating baseline value...')

    if team_1.mapsWon > team_2.mapsWon:
        baseVal1 = 25
        baseVal2 = -25
    else:
        baseVal1 = -25
        baseVal2 = 25
    print('baseVal1:', baseVal1)
    print('baseVal2:', baseVal2)

    li = []
    li.append(baseVal1)
    li.append(baseVal2)
    return li

def expectedScore():
    print('Calculating expected score...')

    expScore1 = 1 / (10 ** ((team_2.rating - team_1.rating) / 400) + 1)
    print('expScore1:', expScore1)
    expScore2 = 1 / (10 ** ((team_1.rating - team_2.rating) / 400) + 1)
    print('expScore2:', expScore2)

    li = []
    li.append(expScore1)
    li.append(expScore2)
    return li

def calculateElo():
    #calculates the new elo for each team
    team1NewRating = round(team_1.rating + (150 * (scoreList[0] - expScoreList[0])) + baseValList[0])
    team2NewRating = round(team_2.rating + (150 * (scoreList[1] - expScoreList[1])) + baseValList[1])

    #calculates elo diff
    eloDiff1 = team1NewRating - team_1.rating
    eloDiff2 = team2NewRating - team_2.rating

    li = []
    li.append(team1NewRating)
    li.append(eloDiff1)
    li.append(team2NewRating)
    li.append(eloDiff2)
    return li

def display():
    line(50)
    print(f'{team_1.name}', '\n', '  New Rating:', eloList[0], '\n', '  Elo Change:', eloList[1])
    print(f'{team_2.name}', '\n',  '  New Rating:', eloList[2], '\n', '  Elo Change:', eloList[3])
    pass

def line(count):
    print('=' * count)

#runs the program

print('Welcome to MFC Elobot 2.0, developed by Zaxosaur.')
line(50)

match_info = []
counter = 0

def main():
    global team_1
    global team_2

    global scoreList
    global baseValList
    global expScoreList
    global eloList

    team_1 = Team.createTeam()
    team_2 = Team.createTeam()

    scoreList = matchScore()
    baseValList = baseline()
    expScoreList = expectedScore()
    eloList = calculateElo()

    calculateElo()
    display()

main()






# counter += 1
# print('Counter =', counter)

dontClose = input('Thanks for using MFC Elobot.')
print(dontClose)
