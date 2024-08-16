import requests


def scrape_team_names() -> list:
    r = requests.get(
        'https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/teams?limit=32')
    resp = r.json()

    team_urls = resp['items']

    teams = []
    for _url in team_urls:
        url = _url['$ref']
        team_info = scrape_team_info(url)
        teams.append(team_info)

    return teams


def scrape_team_info(url: str) -> dict:
    r = requests.get(url)
    resp = r.json()

    team_info = {
        'espn_id': int(resp['id']),
        'slug': resp['slug'],
        'name': resp['displayName'],
        'abbreviation': resp['abbreviation'],
        # Sloppy way to make the url more generic in the
        'url': url.replace('2024', 'YEAR'),
        'home_venue': {
            'name': resp['venue']['fullName'],
            'address': resp['venue']['address']
        },
    }

    return team_info
