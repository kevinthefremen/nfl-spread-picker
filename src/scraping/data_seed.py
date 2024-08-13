from src.db.get_db_client import get_database
import requests


def insert_teams():
    db = get_database()

    teams_collection = db['teams']

    teams_to_insert = get_teams()

    teams_collection.insert_many(teams_to_insert)

    return teams_to_insert


def get_teams() -> list:
    r = requests.get(
        'https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/teams?limit=32')
    resp = r.json()

    team_urls = resp['items']

    teams = []
    for _url in team_urls:
        url = _url['$ref']
        team_info = get_team_info(url)
        teams.append(team_info)

    return teams


def get_team_info(url: str) -> dict:
    r = requests.get(url)
    resp = r.json()

    team_info = {
        'espn_id': int(resp['id']),
        'slug': resp['slug'],
        'name': resp['displayName'],
        'abbreviation': resp['abbreviation'],
        'url': url,
        'home_venue': {
            'name': resp['venue']['fullName'],
            'address': resp['venue']['address']
        },
    }

    return team_info
