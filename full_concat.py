# This is a program for concatenating all .csv files in one
import os
import pandas as pd
files = []
for i in os.walk('Combined_CSV'):
    files.append(i)
extension = 'csv'
for address, dirs, files in files:
    if '.DS_Store' in files:
        files.remove('.DS_Store')
        files = sorted(files)
        combined_csv = pd.concat([pd.read_csv(address + '/' + f) for f in files], ignore_index=True)
        combined_csv.to_csv("full_combined_csv2.csv", index=False)
