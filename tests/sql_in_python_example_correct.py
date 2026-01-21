query = """
    SELECT * FROM languages;
"""

query = '''
    SELECT *
    FROM games
    WHERE test=0
'''

query = """
    SELECT *
    FROM languages;
"""


def get_query1():
    query = f"SELECT MAX(weight) FROM world WHERE ocean='Atlantic'"
    return query


def get_query2():
    limit = 6
    query = f"SELECT speed FROM world WHERE animal='dolphin' LIMIT {limit}"
    return query


def get_query3():
    limit = 6
    query = f"""
    SELECT speed FROM world WHERE animal='dolphin' LIMIT {limit}
    """
    return query


def get_query4():
    query = """
    SELECT speed FROM world WHERE animal='dolphin'
    """
    return query


def return_5():
    query = 'SELECT 5'
    return query


def insert():
    query = '''
    INSERT INTO table_name (column1, column2, column3)
    VALUES (value1, value2, value3);
    '''
    return query


def join():
    query = '''
    SELECT Orders.OrderID, Customers.CustomerName, Orders.OrderDate
    FROM Orders
    INNER JOIN Customers ON Orders.CustomerID=Customers.CustomerID;
    '''
    return query
