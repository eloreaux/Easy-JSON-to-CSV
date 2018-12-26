import argparse
import os
import sys
import json
import pandas as pd
from tqdm import tqdm
import time

from json_to_csv_utils import *

# This is the max quantity of values in the first bucket
# before it is dumped to a larger bucket with 100X capacity.
# This default number has proven to work optimally.
TRANSFERQUANTITY = 1000

parser = argparse.ArgumentParser()
parser.add_argument('json_path',
                    help = "Path to either a JSON file or a directory of JSON files to convert into one csv")
parser.add_argument('--save_path', default = '.', type = str,
                    help = "Path to folder where new csv file will be saved")
parser.add_argument('--filename', default = "json_csv.csv", type = str,
                    help = "Name of new csv file")
parser.add_argument('--repLimit', default = None, type = int,
                    help = "Include this argument to put a limit on the amount of new columns created for lists of values if the stringList argument is not included.")
parser.add_argument('--stringList', dest = "stringList", action='store_true',
                    help = "Include this argument to invoke the 'stringList' functionality, described in the README.txt file")

if __name__ == '__main__':

    args = parser.parse_args()
    json_path = args.json_path
    stringList = args.stringList
    repLimit = args.repLimit

    assert os.path.isdir(json_path) or os.path.isfile(json_path), "Improper file type"

    if os.path.isdir(json_path):
        filenames = [file for file in os.listdir(json_path) if file.endswith(".json")]
    elif os.path.isfile(json_path):
        filenames = [json_path]
        json_path = "."
 
    assert len(filenames) > 0, "No JSON files detected"

    allValues = {}
    allValuesQuantity = 0

    start = time.time()
    for file in filenames:

        print("Opening file {}...".format(file))
        json_file = open(os.path.join(json_path,file))
        jsonObjs = json.load(json_file)
        
        # create a list of buckets, along with list of quantities of each bucket.
        # these will be filled with rows. start with one empty bucket
        buckets = [{}]
        quantities = [0]
        
        # keeping track of the number of rows that have been added to the first bucket
        row = -1
        
        for rowObject in tqdm(jsonObjs):
            row += 1
            
            addRow(rowObject, buckets, row, stringList = stringList, repLimit = repLimit)
            quantities[0] += 1
            
            # check if bucket has filled to max
            if  quantities[0] == TRANSFERQUANTITY:
                # push bucket values to larger bucket, reset row count for first bucket
                valuesPush(buckets, quantities, transferQuantity = TRANSFERQUANTITY)
                row = -1
        
        # empty all buckets into one dictionary
        for i in reversed(range(len(buckets))):
            buckets[i] = dictDump(buckets[i], allValues, quantities[i], allValuesQuantity)
            allValuesQuantity += quantities[i]
        
        sys.stdout.write("\r100%")
        sys.stdout.flush()
        
        print("\n{} rows added from this JSON file.".format(len(jsonObjs)))
        print("Closing file {}...".format(file))
        json_file.close()

    finalFrame = pd.DataFrame(allValues)

    if len(filenames) > 1:
        print("{} rows have been pushed from {} JSON files into a single dataframe.".format(allValuesQuantity, len(filenames)))
    
    end = time.time()
    print("time elapsed: {0:.3f} sec".format(end - start))
    print("writing csv to {}...".format(os.path.join(args.save_path, args.filename)))
    finalFrame.to_csv(os.path.join(args.save_path, args.filename))
    print("complete.")
    
