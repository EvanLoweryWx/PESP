#!/usr/bin/python3
'''
- Determine sample file name by scanning directory for a csv file
- Ingest sammple csv file (sample_fiel_ex_001.csv)
- Store data into two-key dictionary (icao,dateYmd)
- Print out a unique list of icaos
- Print out a unique list of dateYmd
- Loop through dictionary (icao, dateYmd) and print results
'''

## Import csv, os, re modules
import csv
import os
import re

## determine current directory
dir_path = os.path.dirname(os.path.realpath(__file__))

## determine sample file name by scanning directory for a csv file
sample_files = []
for subdir, dirs, files in os.walk(dir_path):
    for cur_name in files:
        cur_file = os.path.join(subdir, cur_name)
        print("checking cur_name({})".format(cur_name))
        
        # Is this file a csv?
        if re.search(r'csv$', cur_name):
            #Yes it is!
            sample_files.append(cur_name)

## Did we find exactly one csv file as we anticipated?
if len(sample_files) != 1:
    print("Error, we did NOT find any sample files ... exiting")
    exit(1)
else:
    print("Well done, you found the following sample files({})".format(sample_files))


## Open csv file and read it into dictionary
# define dictionary
wx_data = {}

# use with so that we don't have to specifically close the file later
with open(sample_files[0], 'r') as f_in:
    
    # use csv module reader function
    reader = csv.reader(f_in)

    # define line number (i)
    i = 0

    # grab headers, iterate line number
    # icao,dateYmd,minTemp,maxTemp,prcp,wspd
    headers = reader.__next__()

    # begin reading file line by line
    # i: line number, start at 1 since 0 was headers
    for row in reader:
        # iterate line number
        i += 1

        # get the first two keys
        key1 = row[0] #header[0] (icao)
        key2 = row[1] #header[1] (dateYmd)

        # have we added these keys to the dictionary before?
        if wx_data.get(key1) is None:
            wx_data[key1] = {}
        if wx_data[key1].get(key2) is None:
            wx_data[key1][key2] = {}

        # store the weather data into the dictionary, loop 
        j = -1
        for header in headers:
            # skip first two headers (already added)
            j += 1
            if j < 2:
                continue

            wx_data[key1][key2][header] = row[j]
            

## print results
for key,val in wx_data.items():
    icao = key
    for key1,val1 in val.items():
        dateYmd = key1
        for key2,val2 in val1.items():
            print("icao({}), dateYmd({}), wxType({}), wxVal({})".format(icao, dateYmd,
                key2, val2))            
