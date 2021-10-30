from pyspark.sql.functions import explode
from pyspark.sql.functions import split
from pyspark.sql.types import StructType
from pyspark.sql.functions import desc

class SparkCountWord:

    def __init__(self, spark_session):
        self.spark = (
            spark_session
            .builder
            .appName("CountWord")
            .config('spark.ui.showConsoleProgress', 'True')
            .getOrCreate()
        )

        self.spark.sparkContext.setLogLevel('ERROR')

    def read_data(self):
        lines = (
            self.spark
            .readStream
            .format('socket')
            .option("host", "localhost")
            .option("port", 9999)
            .load()
        )

        print("Lines: ", lines)

        words = lines.select(
            explode(
                split(lines.value, ' ')
            ).alias('word')
        )

        wordCounts = words.groupBy('word').count().sort(desc('count'))
        #wordCounts = words.groupBy('word').count()
        query = (
            wordCounts
            .writeStream
            .outputMode('complete')
            .format('console')
            .start()
        )

        query.awaitTermination()

    def run(self):
        self.read_data()