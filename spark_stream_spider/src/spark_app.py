from pyspark.sql import SparkSession
import socket

SparkSession.builder.getOrCreate().sparkContext.setLogLevel("ERROR")

from count_word import SparkCountWord

import sys

if __name__ == "__main__":
    spark = (SparkSession.builder.config(
        "spark.serializer",
        "org.apache.spark.serializer.KryoSerializer").getOrCreate())

    loadCountWord = SparkCountWord(spark)
    loadCountWord.run()
