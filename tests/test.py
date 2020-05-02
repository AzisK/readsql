import unittest

import app


class TestRegexes(unittest.TestCase):
    def test_double_select(self):
        sql = app.read('''
            select * from (select * FROM languages) as t
             where gold is not null;    
        '''
        )
        sql_correct = '''
            SELECT * FROM (SELECT * FROM languages) AS t
             WHERE gold IS NOT NULL;    
        '''
        self.assertEqual(sql, sql_correct)

    def test_select_from_groub_by_where(self):
        sql = app.read('''
            select max(height), avg(mass), min(age)  from jungle group by forest where animal=elephant;
        ''')
        sql_correct = '''
            SELECT MAX(height), AVG(mass), MIN(age)  FROM jungle GROUP BY forest WHERE animal=elephant;
        '''
        self.assertEqual(sql, sql_correct)

    def test_is_not_null(self):
        sql = app.read('''
            selECT 1,2,3
            where bounty is null
        ''')
        sql_correct = '''
            SELECT 1,2,3
            WHERE bounty IS NULL
        '''
        self.assertEqual(sql, sql_correct)

    def test_distinct(self):
        sql = app.read('''
            select distinct stars
            from universe
        ''')
        sql_correct = '''
            SELECT DISTINCT stars
            FROM universe
        '''
        self.assertEqual(sql, sql_correct)

    def test_create_table_if_not_exists(self):
        sql = app.read('''
             Create table if not exists `tblsample` (
                `id` VARCHAR(100) NOT NULL auto_increment,
                `name` VARCHAR(120) NOT NULL default 'unknown'
            )
        ''')
        sql_correct = '''
             CREATE TABLE IF NOT EXISTS `tblsample` (
                `id` VARCHAR(100) NOT NULL auto_increment,
                `name` VARCHAR(120) NOT NULL default 'unknown'
            )
        '''
        self.assertEqual(sql, sql_correct)


if __name__ == '__main__':
    unittest.main()
