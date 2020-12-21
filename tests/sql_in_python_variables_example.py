def get_sql():
    limit = 6
    sql = f"SELEct speed from world where animal='dolphin' limit {limit}"
    return sql


def get_query_template():
    limit = 6
    query_template = (
        f"SELEct speed from world where animal='dolphin' group by family limit {limit}"
    )
    return query_template


def get_query():
    limit = 99
    query = f"SELEct speed from world where animal='dolphin' and name is not null group by family limit {limit}"
    return query
