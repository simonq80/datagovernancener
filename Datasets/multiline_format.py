import sys
if len(sys.argv) < 3:
    print('Must give input and output file locations')
    exit()
lines = []
with open(sys.argv[1], "r") as input:
    for line in input:
        lines.append(line)

newlines = []
inquotes = False
buff = ""
for line in lines:
    if line[0] == '"':
        inquotes = True
        line = line[1:]

    if inquotes == False:
        newlines.append(line)

    if inquotes:
        if len(line) > 1 and line[-2] == '"':
            inquotes = False
            line = line[:-2]
            buff += line
            newlines.append(buff.replace("\n", " ") + "\n")
            buff = ""
        else:
            buff += line

outlines = []
for line in newlines:
    outlines.append(line.replace('""', '"'))


with open(sys.argv[2], "w") as output:
    output.writelines(outlines)
