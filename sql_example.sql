select * from languages;

select * from games 
	where test=0;

select * from (select * FROM languages) t;

  select 8 from gg;


select * from (select * FROM languages) as t
  where gold is not null;

selECT 1,2,3
where bounty is null

SELECT couNT(*), Sum(mass)
from universe;

select distinct stars
from universe

SELECT sun from univere group by galaxy

 Create table if not exists `tblsample` (
  `id` VARCHAR(100) NOT NULL auto_increment,
  `name` VARCHAR(120) NOT NULL default 'unknown'
)

select min(date) from calendar

select max(elephant) from jungle group by forest;

SELECT avg(mass) from jungle where animal=gorilla
