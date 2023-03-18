import csv
import pandas as pd

def readCsvFile():
    samples = []
    rows = []
#    with open("dis.csv") as file:
#        csvreader = csv.reader(file)
#        header = []
#        header = next(csvreader)
#        for row in csvreader:
#            rows.append(row)
#        file.close()
    data = pd.read_csv("dis.csv")
    data.columns
    samples = data.Zamkniecie
    return samples


print(readCsvFile())
