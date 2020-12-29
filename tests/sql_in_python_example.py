query = """
    select * from languages;
"""

query = """
    select *
    from games
    where test=0
"""


def get_query():
    query = f"SELEct max(weight) from world where ocean='Atlantic'"
    return query


def get_query():
    limit = 6
    query = f"SELEct speed from world where animal='dolphin' limit {limit}"
    return query


def return_5():
    query = 'select 5'
    return query


def insert():
    query = '''
    insert into table_name (column1, column2, column3)
    values (value1, value2, value3);
    '''
    return query
