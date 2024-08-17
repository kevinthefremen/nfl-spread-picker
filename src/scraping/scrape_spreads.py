import multiprocessing
from pandas import DataFrame
import requests


def scrape_spreads_and_games(teams: DataFrame) -> tuple[list, dict]:
    all_team_spreads = []
    all_games_urls = set()
    for i, team in teams.iterrows():
        #  only goes back to 2012, no idea what bet provider 1002 is but it is default
        spread_url = f'https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/teams/{team['espn_id']}/odds/1002/past-performances?limit=200'  # noqa

        past_spreads = requests.get(spread_url).json()['items']
        print(f'Got {len(past_spreads)} past spreads for {team["name"]}')

        for spread in past_spreads:
            past_game_url = spread['pastCompetition']['$ref']
            all_team_spreads.append({
                'game_url': past_game_url,
                'team': team['_id'],
                'total_line': spread['totalLine'],
                'total_result': spread['totalResult'],
                'ml_odds': spread['moneyLineOdds'],
                'ml_winner': spread['moneylineWinner'],
                'spread': spread['spread'],
                'spread_winner': spread['spreadWinner']
            })

            # we would hit each game twice, once for each team, so this rpevents getting the info twice
            if past_game_url not in all_games_urls:
                all_games_urls.add(past_game_url)

        print(f'Got spreads: {i+1}/{len(teams)}')

    with multiprocessing.Pool() as p:
        print(f'Scraping {len(all_games_urls)} games')
        games = p.map(scrape_single_game, all_games_urls)

    print(f'Got all games')

    return all_team_spreads, games


def scrape_single_game(game_url: str) -> dict:
    past_event = requests.get(game_url).json()

    team_1_score = requests.get(
        past_event['competitors'][0]['score']['$ref']).json()['value']
    team_2_score = requests.get(
        past_event['competitors'][1]['score']['$ref']).json()['value']

    return {
        'url': game_url,
        'espn_id': past_event['id'],
        'date': past_event['date'],
        'venue': {
            'name': past_event['venue']['fullName'],
            'address': past_event['venue']['address'],
            'grass': past_event['venue']['grass'],
            'indoor': past_event['venue']['indoor'],
        },
        'teams': [
            {
                'espn_id': past_event['competitors'][0]['id'],
                'home': past_event['competitors'][0]['homeAway'] == 'home',
                'score': team_1_score,
                'winner': past_event['competitors'][0]['winner'],
            },
            {
                'espn_id': past_event['competitors'][1]['id'],
                'home': past_event['competitors'][1]['homeAway'] == 'home',
                'score': team_2_score,
                'winner': past_event['competitors'][1]['winner'],
            }
        ]
    }
