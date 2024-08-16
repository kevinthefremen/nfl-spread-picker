from src.scraping.scrape_rosters import scrape_coach, scrape_athletes, scrape_single_team_single_season_roster, scrape_single_athlete
from pandas import DataFrame


def test_scrape_coach():
    coaches_url = 'http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/teams/22/coaches'

    coach = scrape_coach(coaches_url)

    assert coach['espn_id'] == 17751
    assert coach['full_name'] == 'Jonathan Gannon'
    assert coach['experience'] == 1


def test_scrape_atheletes():
    athletes_url = 'http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/teams/22/athletes?limit=1000'

    athletes = scrape_athletes(athletes_url)

    assert len(athletes) == 92
    # Check that an expected athelete is in the results
    athletes_df = DataFrame(athletes)
    assert athletes_df.query('espn_id == 5084939')[
        'full_name'].values[0] == 'Isaiah Adams'


def test_scrape_single_season():
    roster = scrape_single_team_single_season_roster(22, 2024)

    assert len(roster['athletes']) == 92
    assert roster['coach']['full_name'] == 'Jonathan Gannon'


def test_scrape_single_athlete():
    athelete = scrape_single_athlete(
        'http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2021/athletes/4361027?lang=en&region=us')

    assert athelete == {
        'espn_id': 4361027,
        'full_name': 'Thomas Yassmin',
        'weight': 251,
        'height': 77,
        'age': 24,
        'experience': 0
    }
