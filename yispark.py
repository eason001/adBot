from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.ml.feature import PCA
from pyspark.mllib.feature import PCA as PCAmllib
from pyspark.mllib.linalg import Vectors

sc = SparkContext()
sqlContext = SQLContext(sc)
lines = sc.textFile("/mnt/yi-ad-proj/compressed_data/compressed_data")

#lines = sc.textFile("/home/ubuntu/yi/t.txt",5)
#words = lines.flatMap(lambda x:x.split(" "))
#word_count = (words.map(lambda x: (x,1)).reduceByKey(lambda x, y:x + y))
#word_count.repartition(1).saveAsTextFile("/home/ubuntu/yi/out",mode='overwrite')

split_lines = lines.map(lambda x:x.split(" "))
float_lines = split_lines.map(lambda x:[x[0]]+([float(y) for y in x[1:]]))
#test = clean_lines.take(10)
#for x in test:
#	print x[0]

###with ml
#clean_lines = split_lines.map(lambda x:[float(y) for y in x[1:]])
#clean_lines = float_lines.map(lambda x:Vectors.dense(x[1:]))
#df = sqlContext.createDataFrame(clean_lines,["features"])
#pca = PCA(k=10,inputCol="features", outputCol="pca_features")
#model = pca.fit(df)
#model.transform(df).collect()[0].pca_features


###with mllib
clean_lines = float_lines.map(lambda x:Vectors.dense(x[1:]))
model = PCAmllib(10).fit(clean_lines)
#transformed = model.transform(clean_lines)
