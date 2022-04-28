# This is a program for concatenating .csv files from same date
import os
import pandas as pd
files = []
for i in os.walk('CSV'):
    files.append(i)
extension = 'csv'
for address, dirs, files in files:
    path = 'Combined_CSV' + '/' + address[4:]
    if not os.path.exists(path):
        os.makedirs(path)
    if '.DS_Store' not in files:
        combined_csv = pd.concat([pd.read_csv(address + '/' + f) for f in files], ignore_index=True)
        # export to csv
        combined_csv.to_csv(f"{address[4:]}combined_csv.csv")


