from bs4 import BeautifulSoup
import requests
from difflib import SequenceMatcher


# ------------------------------------
#           BASIC INFO
# - all func outputs are strings
# - input is always the home-team
# - "NP" stands for: not playing
# - "HF" stands for: half time
# ------------------------------------

URL = "https://www.livescores.com/soccer/live/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}


# basic setup for other functions
def setup():
    page = requests.get(URL , headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    # define team you wanna know
    pos = -1
    # gets all scores
    allTeams = soup.findAll("div", {"class": "tright"})
    return (soup, pos, allTeams)


# returns current score of playing team
def get_score(team):
    soup, pos, allTeams = setup()

    # checks if list is empty
    if not allTeams:
        print("Momentan spielt kein Team!")
        quit()

    best_ratio = 0
    valid_team = team

    # finds matching team out of all teams
    for i, t in enumerate(allTeams):
        t = t.text[1:-1]
        ratio = SequenceMatcher(None, t, team).ratio()
        if  ratio > 0.55 and ratio > best_ratio:
            valid_team = t
            best_ratio = ratio
            pos = i
    
    # checks if teams is playing
    if pos == -1:
        return "NP"

    allScores = soup.findAll("div", {"class": "sco"})
    score = allScores[pos].text[1:-1]
    return score


# returns current minute of game
def get_minute(team):
    soup, pos, allTeams = setup()

    # checks if list is empty
    if not allTeams:
        print("Momentan spielt kein Team!")
        quit()

    best_ratio = 0
    valid_team = team

    # finds matching team out of all teams
    for i, t in enumerate(allTeams):
        t = t.text[1:-1]
        ratio = SequenceMatcher(None, t, team).ratio()
        if  ratio > 0.6 and ratio > best_ratio:
            valid_team = t
            best_ratio = ratio
            pos = i

    # checks if teams is playing
    if pos == -1:
        return "NP"

    # scrapes minute from html and formats it
    all_minutes = soup.findAll("div", {"class": "min"})
    minute = all_minutes[pos].text[1:-1]
    minute = minute.replace("'", "")
    return minute


# gets name of opponent team | input is home team
def get_opponent(team):
    soup, pos, allTeams = setup()

    # checks if list is empty
    if not allTeams:
        print("Momentan spielt kein Team!")
        quit()

    best_ratio = 0
    valid_team = team

    # finds matching team out of all teams
    for i, t in enumerate(allTeams):
        t = t.text[1:-1]
        ratio = SequenceMatcher(None, t, team).ratio()
        if  ratio > 0.6 and ratio > best_ratio:
            valid_team = t
            best_ratio = ratio
            pos = i

    # checks if teams is playing
    if pos == -1:
        return "NP"

    # scrapes opponent from html and formats it
    all_opponents = soup.findAll("div", {"class": "name"})
    opponent = all_opponents[pos*2+1].text[1:-1]
    return opponent



team = input("Enter a team name: ")
print("Opponent: " + get_opponent(team) + " | Score: " + get_score(team) + " | Minute: " + get_minute(team))


input("Press Enter key to exit... ")
quit()