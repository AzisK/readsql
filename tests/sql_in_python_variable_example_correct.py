def get_query():
    limit = 6
    sql = f"SELECT speed FROM world WHERE animal='dolphin' LIMIT {limit}"
    return sql
