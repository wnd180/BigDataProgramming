#-*- coding:utf-8 -*-

from pyspark.sql import *



if __name__ == "__main__":
    spark = SparkSession.builder.appName("homeprice").getOrCreate()

    df1 = spark.read.load("hdfs:///user/maria_dev/2012.csv", format="csv", sep= ',', inferSchema = "true", header= "true")
    df2 = spark.read.load("hdfs:///user/maria_dev/2021.csv", format="csv", sep= ',', inferSchema = "true", header= "true")

    df1.createOrReplaceTempView("home2012")
    df2.createOrReplaceTempView("home2021")

    result = spark.sql("""
        select t1.region_name, t1.p1, t2.p2, t2.p2/t1.p1 as inc
        from (select home2012.region_name, avg(home2012.per_price) as p1
        from home2012 
        group by home2012.region_name) t1,
        (select home2021.region_name, avg(home2021.per_price) as p2
        from home2021
        group by home2021.region_name) t2
        where t1.region_name = t2.region_name
        order by inc desc limit 10
        """)

    result.write.csv("hdfs:///user/maria_dev/2012to2021/")
    for row in result.collect():
        print(row)