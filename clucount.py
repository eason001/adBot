import sys

filepath = sys.argv[1]
k = sys.argv[2]
output = []
file = open(filepath,'r')
count = 0
for i in range(int(k)):
	output.append(0)
for line in file:
	count += 1
	for i in range(int(k)):
		if count == 1:
			WSSSE = line.split("=")[1]
		else:
			if line.split(" ")[1]==str(i)+"\n":
				output[i]+=1
WSSSE_AVG = float(WSSSE) / (count-1)
print "number of data: " + str(count-1)
print "WSSSE: " + WSSSE
print "WSSSE AVG: " + str(WSSSE_AVG)
for i in range(int(k)):
	print str(i) + ": " + str(output[i])
