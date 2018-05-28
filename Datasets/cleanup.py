import sys
import re
if len(sys.argv) < 3:
    print('Must give input and output file locations')
    exit()

filesize = 400

lines = []
with open(sys.argv[1], "r") as input:
    for line in input:
        #TODO: Proper regex to do this
        l = line.replace('< ', '<')
        l = l.replace(' >', '>')
        lines.append(line)

towrite = []
for i in range(0, int(len(lines)/filesize) + 1):
    towrite.append(lines[i*filesize:i*filesize+filesize])

i = 0
for f in towrite:
    with open(sys.argv[2] + str(i) + ".txt", "w") as output:
        output.writelines(f)
    i+=1
