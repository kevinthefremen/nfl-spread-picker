from src.db.get_db_client import get_database
import requests
from src.scraping.scrape_rosters import scrape_rosters
from src.config import START_YEAR, END_YEAR
from src.db.teams import get_all_teams
from src.scraping.scrape_teams import scrape_team_names


def insert_teams():
    db = get_database()

    teams_collection = db['teams']

    teams_to_insert = scrape_team_names()

    teams_collection.insert_many(teams_to_insert)

    return teams_to_insert


def insert_rosters():
    db = get_database()
    teams = get_all_teams(db)

    rosters = scrape_rosters(teams, START_YEAR, END_YEAR)

    rosters_collection = db['rosters']
    rosters_collection.insert_many(rosters)
