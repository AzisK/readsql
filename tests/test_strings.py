import argparse

import readsql.__main__ as rsql
from tests.timing import timing


@timing
def test_double_select():
    sql = rsql.read_replace(
        '''
        select * from (select * FROM languages) as t
         where gold is not null;
    '''
    )
    sql_correct = '''
        SELECT * FROM (SELECT * FROM languages) AS t
         WHERE gold IS NOT NULL;
    '''
    sql == sql_correct


@timing
def test_select_from_groub_by_where():
    sql = rsql.read_replace(
        '''
        select max(height), avg(mass), min(age)  from jungle group by forest where animal=elephant;
    '''
    )
    sql_correct = '''
        SELECT MAX(height), AVG(mass), MIN(age)  FROM jungle GROUP BY forest WHERE animal=elephant;
    '''
    assert sql == sql_correct


@timing
def test_is_not_null():
    sql = rsql.read_replace(
        '''
        selECT 1,2,3
        where bounty is null
    '''
    )
    sql_correct = '''
        SELECT 1,2,3
        WHERE bounty IS NULL
    '''
    assert sql == sql_correct


@timing
def test_distinct():
    sql = rsql.read_replace(
        '''
        select distinct stars
        from universe
    '''
    )
    sql_correct = '''
        SELECT DISTINCT stars
        FROM universe
    '''
    assert sql == sql_correct


@timing
def test_create_table_if_not_exists():
    sql = rsql.read_replace(
        '''
         Create table if not exists `tblsample` (
            `id` VARCHAR(100) NOT NULL auto_increment,
            `name` VARCHAR(120) NOT NULL default 'unknown'
        )
    '''
    )
    sql_correct = '''
         CREATE TABLE IF NOT EXISTS `tblsample` (
            `id` VARCHAR(100) NOT NULL auto_increment,
            `name` VARCHAR(120) NOT NULL default 'unknown'
        )
    '''
    assert sql == sql_correct


@timing
def test_command_line_string():
    sql = 'select sushi from tokyo'

    args = argparse.Namespace(
        nothing=False,
        path=[sql],
        python_var=['query'],
        string=True,
    )

    sql_adjusted = rsql.read_replace(args.path[0])

    sql_correct = 'SELECT sushi FROM tokyo'

    assert sql_adjusted == sql_correct


@timing
def test_command_line_strings():
    sql1 = '''
        select * from (select * FROM languages) as t
         where gold is not null;
    '''

    sql2 = 'selecT 99 from hundred'

    args = argparse.Namespace(
        nothing=False,
        path=[sql1, sql2],
        python_var=['query'],
        string=True,
    )

    sql_adjusted = [rsql.read_replace(s) for s in args.path]

    sql_correct1 = '''
        SELECT * FROM (SELECT * FROM languages) AS t
         WHERE gold IS NOT NULL;
    '''
    sql_correct2 = 'SELECT 99 FROM hundred'
    sql_correct = [sql_correct1, sql_correct2]

    assert str(sql_adjusted) == str(sql_correct)
