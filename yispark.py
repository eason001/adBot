from pyspark import SparkContext
from pyspark.sql import SQLContext, Row
from pyspark.ml.feature import PCA
from pyspark.mllib.feature import PCA as PCAmllib
from pyspark.mllib.linalg import Vectors
from pyspark import SparkConf, SparkContext
from pyspark.ml.clustering import KMeans

###PCA with ml
def pca(df):
	pca = PCA(k=10,inputCol="features", outputCol="pca_features")
	model = pca.fit(df)
#	outData = model.transform(lines)
	pcaFeatures = model.transform(lines).select("labels","pca_features")
	dfwrite(pcaFeatures,'pcaFeatures')

###with mllib
#lines = lines.map(lambda x:Vectors.dense(x))
#model = PCAmllib(10).fit(lines)
#outData = model.transform(lines)
#outData.repartition(1).saveAsTextFile("/home/ubuntu/yi/out",mode='overwrite')

###Kmeans with ml
def kmeans(df):
	kmeans = KMeans(k=2,seed=1)
	model = kmeans.fit(df)
	centers = model.clusterCenters()
	print len(centers)
	kmFeatures = model.transform(df).select("features", "prediction")
	dfwrite(kmFeatures,'kmFeatures')	

###Write out
def dfwrite(df,dirname):
	df.rdd.repartition(1).saveAsTextFile("/home/ubuntu/yi/" + dirname)
def rddwrite(rdd,dirname):
	rdd.repartition(1).saveAsTextFile("/home/ubuntu/yi/" + dirname)


###Separate clustering results in different folders
def separate():
	import os
	img_path = "/mnt/yi-ad-proj/clean_data/img/"
	compress_path = "/home/ubuntu/yi/pcaFeatures/pca_data"
	compress_data = open(compress_path,'r')
	cluster_path = "/home/ubuntu/yi/clusterFeatures/cluster_data"
	cluster_data = open(cluster_path,'r')
	cdata = []
	for x in compress_data:
		cdata.append(x.split(" ")[0])
	i = 0
	
        for x in cluster_data:
		file = cdata[i]+'.png'
		
		try:
		    if x == '0\n':
			os.system('sudo mv ' + img_path + file + ' ' + img_path + 'one/')
		    if x == '1\n':
			os.system('sudo mv ' + img_path + file + ' ' + img_path + 'two/')
		except:
		    print file + ' failed'
		    continue
		i += 1
	print "separation finished~"


def finder():
	import os
	img_path = "/mnt/yi-ad-proj/clean_data/img/"
	compress_path = "/mnt/yi-ad-proj/compressed_data/compressed_data"
	compress_data = open(compress_path,'r')
	cluster_path = "/home/ubuntu/yi/clusterFeatures/cluster_data"
	cluster_data = open(cluster_path,'r')
	cdata = []
	for x in compress_data:
#	for file in os.listdir(img_dir):
		file = x.split(" ")[0] + '.png'
		try:
			os.system('sudo rm ' + img_path + file)
		except:
		    print file + ' failed'
		    continue
	print "finding finished~"
#	os.system("export _JAVA_OPTIONS='-Xms1g -Xmx40g'")	

def iniPCA():
	conf = (SparkConf().set("spark.driver.maxResultSize", "5g"))
	sc = SparkContext(conf=conf)
	sqlContext = SQLContext(sc)
	data = sc.textFile("/mnt/yi-ad-proj/compressed_data/compressed_data").map(lambda x:x.split(" ")).cache()
	data = data.map(lambda x:(x[0],[float(y) for y in x[1:]]))
	df = data.map(lambda x: Row(labels=x[0],features=Vectors.dense(x))).toDF()
	return df

def iniKM():
	conf = (SparkConf().set("spark.driver.maxResultSize", "5g"))
	sc = SparkContext(conf=conf)
	sqlContext = SQLContext(sc)
	data = sc.textFile("/mnt/yi-ad-proj/reduced_data/reduced_data").map(lambda x:x.split(" ")).cache()
	data = data.map(lambda x:[float(y) for y in x])
	df = data.map(lambda x: Row(features=Vectors.dense(x))).toDF()
	return df

if __name__=="__main__":
	
#	df = iniPCA()
#        pca(df)
	#kmeans(df)
	separate()
#	finder()
