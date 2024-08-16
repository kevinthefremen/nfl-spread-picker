from src.scraping.scrape_teams import scrape_team_info, scrape_team_names


def test_get_team_info():
    test_url_cardinals = 'http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/teams/22?lang=en&region=us'
    res = scrape_team_info(test_url_cardinals)

    assert res == {'espn_id': 22, 'slug': 'arizona-cardinals', 'name': 'Arizona Cardinals', 'abbreviation': 'ARI',
                   'url': 'http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/teams/22?lang=en&region=us',
                   'home_venue': {'name': 'State Farm Stadium', "address": {
                       "city": "Glendale",
                       "state": "AZ",
                       "zipCode": "85305"
                   }}}


def test_get_teams():
    res = scrape_team_names()

    assert len(res) == 32
