import os
import pandas as pd

# this script will convert all xlsx files in a directory to csv files
# the xlsx files have multiple sheets, each sheet will be converted to a csv file

directory = "docs/udyan"

for filename in os.listdir(directory):
    if filename.endswith(".xlsx"):
        file_path = os.path.join(directory, filename)
        # read xlsx file
        df = pd.read_excel(file_path, sheet_name=None)
        # convert each sheet to csv file
        for sheet_name in df.keys():
            df[sheet_name].to_csv(
                os.path.join(directory, sheet_name + ".csv"), index=False
            )
        
        # delete xlsx file
        os.remove(file_path)
    else:
        continue
