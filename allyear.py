#-*- coding:utf-8 -*-

from pyspark.sql import *



if __name__ == "__main__":
    spark = SparkSession.builder.appName("allhomeprice").getOrCreate()

    df1 = spark.read.load("hdfs:///user/maria_dev/data/merge.csv", format="csv", sep= ',', inferSchema = "true", header= "true")

    df1.createOrReplaceTempView("merge")

    result = spark.sql("""
        select year, region_name, avg(per_price) as alldata
        from merge
        group by year,region_name
        order by alldata desc limit 50
        """)

    result.write.csv("hdfs:///user/maria_dev/total/")
    for row in result.collect():
        print(row)