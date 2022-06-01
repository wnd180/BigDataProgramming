select region_name, avg(per_price)
from home2012
group by region_name;

(select region_name, avg(per_price)
from home2019
group by region_name);

select home2012.region_name, avg(home2012.per_price), avg(home2019.per_price)
from home2012 left join (select region_name, avg(per_price) from home2019 group by region_name) on home2012.region_name = home2019.region_name
group by region_name;

select *
from
(
    (select region_name,avg(per_price)
    from home2012
    group by region_name) AS tb1,
    (select region_name, avg(per_price)
    from home2019
    group by region_name) AS tb2
    );


SELECT
    t2012.region_name, t2012.avgprice2012, t2019.avgprice2019
FROM
    (SELECT 
        home2012.region_name, AVG(home2012.per_price) avgprice2012
    FROM
        home2012
    GROUP BY region_name) AS t2012
        LEFT JOIN
    (SELECT 
        region_name, AVG(per_price) avgprice2019
    FROM
        home2019
    GROUP BY region_name) AS t2019 ON t2012.region_name = t2019.region_name
;
