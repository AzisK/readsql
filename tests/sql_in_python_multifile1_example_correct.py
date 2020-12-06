query = """
    SELECT * FROM languages;
"""

query = """
    SELECT *
    FROM games
    WHERE test=0
"""


def get_query1():
    query = (
        f"SELECT MAX(weight) FROM world WHERE ocean='Atlantic' and water in NOT null"
    )
    return query


def get_query2():
    limit = 6
    query = f"SELECT speed FROM world WHERE animal='dolphin' LIMIT {limit}"
    return query


def get_query3():
    query = 'SELECT 5'
    return query
