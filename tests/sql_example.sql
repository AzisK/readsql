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

select max(height), avg(mass), min(age)  from jungle group by forest where animal=elephant;

insert into table_name (column1, column2, column3)
values (value1, value2, value3);

select Orders.OrderID, Customers.CustomerName, Orders.OrderDate
from Orders
inner join Customers on Orders.CustomerID=Customers.CustomerID;
