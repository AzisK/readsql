def get_query():
    limit = 6
    sql = f"SELEct speed from world where animal='dolphin' limit {limit}"
    return sql
