import readsql.__main__ as rsql
from tests.timing import timing


@timing
def test_double_select():
    sql = rsql.read(
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
    sql = rsql.read(
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
    sql = rsql.read(
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
    sql = rsql.read(
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
    sql = rsql.read(
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
