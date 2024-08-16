import requests
from pandas import DataFrame, Series
import multiprocessing


def scrape_rosters(teams: DataFrame, start_year: int, end_year: int):
    rosters = []
    for i, team in teams.iterrows():
        single_team_rosters = scrape_single_team_rosters(
            team, start_year, end_year)
        rosters.extend(single_team_rosters)
        print(f'Completed: {i+1}/{len(teams)}')

    return rosters


def scrape_single_team_rosters(team: Series, start_year: int, end_year: int):
    single_team_rosters = []

    for year in range(start_year, end_year+1):
        season_roster = scrape_single_team_single_season_roster(
            team['espn_id'], team['_id'], year)
        single_team_rosters.append(season_roster)

    print(f'Got all rosters for {team["name"]}')
    return single_team_rosters


def scrape_single_team_single_season_roster(team_espn_id: int, team_object_id, year: int):
    athletes_url = f'https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{year}/teams/{team_espn_id}/athletes?limit=1000'  # noqa
    coach_url = f'http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{year}/teams/{team_espn_id}/coaches'  # noqa

    athletes = None
    coach = None

    try:
        athletes = scrape_athletes(athletes_url)
        coach = scrape_coach(coach_url)
    except Exception as e:
        print(f'Failed to get roster for {year} for team {team_espn_id}')
        print(e)
        return {'team_id': team_object_id,
                'year': year,
                'athletes': athletes or None,
                'coach': coach or None
                }

    print(f'Got roster for {year} for team {team_espn_id}')
    return {'team_id': team_object_id,
            'year': year,
            'athletes': athletes,
            'coach': coach
            }


def scrape_athletes(athletes_url: str):
    # add extreme limit to the url to make sure we get the full roster
    r = requests.get(athletes_url)
    resp = r.json()

    urls = resp['items']

    with multiprocessing.Pool() as p:
        roster = p.map(scrape_single_athlete, (url['$ref'] for url in urls))

    return roster


def scrape_single_athlete(url: str):
    try:
        athlete = requests.get(url).json()
        # some cases this field does not exist
        age = athlete.get('age', None)
        athlete_info = {
            'espn_id': int(athlete['id']),
            'full_name': athlete['fullName'],
            'weight': athlete['weight'],
            'height': athlete['height'],
            'age': age,
            'experience': athlete['experience']['years'],
        }
        return athlete_info
    except Exception as e:
        print(f'Failed to get athlete from {url}')
        print(e)
        return None


def scrape_coach(coach_url: str):
    r = requests.get(coach_url)
    resp = r.json()

    _url = resp['items'][0]['$ref']
    coach = requests.get(_url).json()

    return {
        'espn_id': int(coach['id']),
        'full_name': coach['firstName'] + ' ' + coach['lastName'],
        'experience': coach['experience']
    }
