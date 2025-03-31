import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, when, concat, count
import pandas as pdfrom
from delta import configure_spark_with_delta_pip


builder = SparkSession.builder \
    .appName("AdventureWorks Ingestion") \
    .master("local[*]") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0") \
    .config("spark.jars", "/Users/cezartipa/Downloads/mssql-jdbc-12.10.0.jre8.jar") \

spark = configure_spark_with_delta_pip(builder).getOrCreate()

jdbc_url = "jdbc:sqlserver://192.168.0.207:1433;databaseName=AdventureWorks2022"
connection_properties = {
    "encrypt": "true",
    "trustServerCertificate": "true",
    "user": "cezar",
    "password": "Verte#123",
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
}
df = spark.read.jdbc(
    url=jdbc_url, table="Person.Person", properties=connection_properties)

df.select([count(when(col(c).isNull(), c)).alias(c)
          for c in df.columns]).show()

df = df.withColumn("Title", when(col("Title").isNull(),
                   lit("-")).otherwise(col("Title")))


df.write.format("delta").mode("overwrite").save(
    "/Users/cezartipa/Downloads/delta-table")
df = spark.read.format("delta").load("/Users/cezartipa/Downloads/delta-table")
# df.show()
df.write \
  .mode("overwrite") \
  .jdbc(url=jdbc_url, table="Person.Person_Updated", properties=connection_properties)
