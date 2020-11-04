import read_csv
import csv
l = read_csv.readCSV2('labels.txt')
titles = []
# 2194 2177
print(len(l))
nl = []
for i in l:
    if i[0] not in titles:
        titles.append(i[0])
        nl.append(i)
print(len(l))
print(len(titles))
print(len(nl))
with open('labelsn.txt', 'w') as csvfile:
    w = csv.writer(csvfile, delimiter=' ')
    for row in nl:
        w.writerow(row)
