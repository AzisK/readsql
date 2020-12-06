def get_sql():
    limit = 6
    sql = f"SELECT speed FROM world WHERE animal='dolphin' LIMIT {limit}"
    return sql


def get_query_template():
    limit = 6
    query_template = (
        f"SELECT speed FROM world WHERE animal='dolphin' GROUP BY family LIMIT {limit}"
    )
    return query_template


def get_query():
    limit = 99
    query = f"SELECT speed FROM world WHERE animal='dolphin' AND name IS NOT NULL GROUP BY family LIMIT {limit}"
    return query
