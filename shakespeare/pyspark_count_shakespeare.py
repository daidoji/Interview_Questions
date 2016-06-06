#!/usr/bin/python

import pyspark
import pyspark_csv as pycsv

sc = pyspark.SparkContext()
sqlCtx = pyspark.sql.SQLContext(sc) or pyspark.HiveContext(sc)

plaintext = sc.textFile('gs://bill-shakespeare-bucket/will_play_text.csv')
col_names = ['id','Play','Act','Line_Number','Character', 'Line']
dataframe = pycsv.csvToDataFrame(sqlCtx, plaintext, columns=col_names,
                                 sep=';', parseDate=False)
# Filter only lines with characters saying words
# One should notice that only lines actually said by actors contain actual
# numbers in that column.
dataframe = dataframe.filter(dataframe["Line_Number"] != "")
lines_said = dataframe.select(dataframe["Line"])
# From here its a simple functional job to get words longer than 4 characters,
# lowercase them all for uniformity, then count and sort
wordcounts = lines_said.flatMap(lambda rec: rec.Line.split(" ")) \
        .map(lambda word: word.lower()) \
        .filter(lambda word: len(word) > 4) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda x,y: x+y) \
        .map(lambda x: (x[1], x[0])) \
        .sortByKey(ascending=False) \
        .take(10)

stmt = "The most common word greater than 4 characters is {}"
print stmt.format(wordcounts[0])
