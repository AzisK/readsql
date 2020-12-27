SELECT * FROM languages;

SELECT * FROM games
	WHERE test=0;

SELECT * FROM (SELECT * FROM languages) t;

  SELECT 8 FROM gg;


SELECT * FROM (SELECT * FROM languages) AS t
  WHERE gold IS NOT NULL;

SELECT 1,2,3
WHERE bounty IS NULL

SELECT COUNT(*), SUM(mass)
FROM universe;

SELECT DISTINCT stars
FROM universe

SELECT sun FROM univere GROUP BY galaxy

 CREATE TABLE IF NOT EXISTS `tblsample` (
  `id` VARCHAR(100) NOT NULL auto_increment,
  `name` VARCHAR(120) NOT NULL default 'unknown'
)

SELECT MAX(height), AVG(mass), MIN(age)  FROM jungle GROUP BY forest WHERE animal=elephant;
