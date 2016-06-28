from pyspark import SparkContext
from pyspark.sql import SQLContext, Row
from pyspark.ml.feature import PCA
from pyspark.mllib.feature import PCA as PCAmllib
from pyspark.mllib.linalg import Vectors
from pyspark import SparkConf, SparkContext

conf = (SparkConf().set("spark.driver.maxResultSize", "5g"))
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)
lines = sc.textFile("/mnt/yi-ad-proj/compressed_data/compressed_data").map(lambda x:x.split(" ")).cache()
lines = lines.map(lambda x:[float(y) for y in x[1:]])

###with ml
lines = lines.map(lambda x: Row(features=Vectors.dense(x))).toDF()
pca = PCA(k=10,inputCol="features", outputCol="pca_features")
model = pca.fit(lines)
outData = model.transform(lines)
pcaFeatures = model.transform(lines).select("pca_features")

###with mllib
#lines = lines.map(lambda x:Vectors.dense(x))
#model = PCAmllib(10).fit(lines)
#outData = model.transform(lines)
#outData.repartition(1).saveAsTextFile("/home/ubuntu/yi/out",mode='overwrite')

###Write out
outData.rdd.repartition(1).saveAsTextFile("/home/ubuntu/yi/outData")
pcaFeatures.rdd.repartition(1).saveAsTextFile("/home/ubuntu/yi/pcaFeatures")
