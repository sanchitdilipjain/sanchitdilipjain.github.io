import os
import sys
import pyspark.sql.functions as F
from pyspark.sql import SparkSession

if __name__ == "__main__":
    """
        Usage: wordcount [destination path]
    """
    spark = SparkSession\
        .builder\
        .appName("WordCount")\
        .getOrCreate()

    s3_path = None

    if len(sys.argv) > 1:
        s3_path = sys.argv[1]
    else:
        print("S3 output location not specified printing top 10 results to output stream")

    text_file = spark.sparkContext.textFile(s3_path+"/input")
    counts = text_file.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b).sortBy(lambda x: x[1], False)
    counts_df = counts.toDF(["word","count"])

    if s3_path:
        counts_df.write.mode("overwrite").csv(s3_path + "/output")
        print("WordCount job completed successfully. Refer output at S3 path: " + s3_path+ "/output")
    else:
        counts_df.show(10, False)
        print("WordCount job completed successfully.")

    spark.stop()