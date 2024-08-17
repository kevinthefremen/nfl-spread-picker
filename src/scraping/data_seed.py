from src.db.get_db_client import get_database
import requests
from src.scraping.scrape_rosters import scrape_rosters
from src.config import START_YEAR, END_YEAR
from src.db.teams import get_all_teams
from src.scraping.scrape_teams import scrape_team_names
from src.scraping.scrape_spreads import scrape_spreads_and_games


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


def insert_past_spreads():
    db = get_database()
    teams = get_all_teams(db)

    spreads, games = scrape_spreads_and_games(teams)

    games_collection = db['games']
    games_collection.insert_many(games)
    print(f'Inserted {len(games)} games')

    # after inserting the games, line up the spreads with the game ids
    for spread in spreads:
        game_url = spread['game_url']
        game = games_collection.find_one({'url': game_url})
        spread['game_id'] = game['_id']

    spreads_collection = db['spreads']
    spreads_collection.insert_many(spreads)
    print(f'Inserted {len(spreads)} spreads')
