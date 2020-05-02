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


if __name__ == '__main__':
    unittest.main()
