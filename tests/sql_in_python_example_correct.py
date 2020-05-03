query = """
    SELECT * FROM languages;
"""

query = """
    SELECT * 
    FROM games 
    WHERE test=0
"""


def get_query():
    limit = 6
    query = f"SELECT MAX(weight) FROM world WHERE ocean='Atlantic'"
    return query


def get_query():
    query = f"SELECT speed FROM world WHERE animal='dolphin' limit {limit}"
    return query


def return_5():
    query = 'SELECT 5'
    return query
