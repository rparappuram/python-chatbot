import os
import pandas as pd

# this script will convert all xlsx files in a directory to csv files

directory = "../docs2"

# loop through all files in directory
for filename in os.listdir(directory):
    # check if file is an xlsx file
    if filename.endswith(".xlsx"):
        # read xlsx file
        df = pd.read_excel(os.path.join(directory, filename))
        # save as csv file
        df.to_csv(os.path.join(directory, filename[:-5] + ".csv"), index=False)
        # delete xlsx file
        os.remove(os.path.join(directory, filename))

    else:
        continue
