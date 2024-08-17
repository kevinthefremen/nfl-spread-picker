from src.scraping.scrape_spreads import scrape_single_game, scrape_spreads_and_games


def test_scrape_spreads():
    res = scrape_spreads_and_games({'espn_id': 1, '_id': 1})

    assert len(res) == 175


def test_scrape_single_game():
    past_event_url = 'http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/320909012/competitions/320909012?lang=en&region=us'

    res = scrape_single_game(past_event_url)

    assert res == {'espn_id': '320909012', 'date': '2012-09-09T17:00Z',
                   'venue': {
                       'name': 'GEHA Field at Arrowhead Stadium',
                       'address': {
                           'city': 'Kansas City',
                           'state': 'MO',
                           'zipCode': '64129'
                       },
                       'grass': True,
                       'indoor': False
                   },
                   'teams': [
                       {
                           'espn_id': '12', 'home': True,
                           'score': 24.0, 'winner': False
                       },
                       {
                           'espn_id': '1', 'home': False,
                           'score': 40.0, 'winner': True
                       }
                   ]
                   }
