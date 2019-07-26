from datetime import datetime
from os import walk
import csv
import os.path

f = []
for (dirpath, dirnames, filenames) in walk("./"):
    f.extend(filenames)
    break

dataFiles = []
for file in f:
    if ".csv" in file and '_Fluxbot_Data_' in file and not "_Dated" in file and not os.path.exists(file[:-4] + "_Dated.csv"):
        dataFiles.append(file)

print(dataFiles)

for file in dataFiles:
    with open(file,'r') as csvinput:
        with open(file[:-4] + "_Dated.csv", 'w') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            reader = csv.reader(csvinput)

            all = []
            row = next(reader)
            row.append('Year')
            row.append('Month')
            row.append('Day')
            row.append('Hour')
            row.append('Minute')
            row.append('Second')
            all.append(row)

            for row in reader:
                time = datetime.utcfromtimestamp(int(row[0]))
                row.append(time.strftime("%Y"))
                row.append(time.strftime("%m"))
                row.append(time.strftime("%d"))
                row.append(time.strftime("%H"))
                row.append(time.strftime("%M"))
                row.append(time.strftime("%S"))
                all.append(row)

            writer.writerows(all)
