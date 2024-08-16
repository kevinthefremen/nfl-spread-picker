from pymongo import database
from pandas import DataFrame


def get_all_teams(db) -> DataFrame:
    teams_collections = db['teams']
    teams = teams_collections.find({})

    return DataFrame(teams)
