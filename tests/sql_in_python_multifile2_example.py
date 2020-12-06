query = """
    select * from languages;
"""

query = """
    select *
    from games
    where test=0
"""


def get_query1():
    query = (
        f"SELEct max(weight) from world where ocean='Atlantic' and water is not null"
    )
    return query


def get_query2():
    limit = 6
    query = f"SELEct speed from world where animal='dolphin' limit {limit}"
    return query


def get_query3():
    query = 'select 5'
    return query
