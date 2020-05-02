select * from languages;

select * from games 
	where test=0;

select * from (select * FROM languages) t;

  select 8 from gg;


select * from (select * FROM languages) as t
  where gold is not null;
