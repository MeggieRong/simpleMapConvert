#!/bin/bash

filename=output_files/state_points.json

#快速解析jason格式
cat $filename |  grep "state id" |  awk -F '[":,]' '{print $4}' > state_id.csv
cat  $filename |  grep "theta"   | awk -F '[":,]' '{print $4}' | awk -F '[ ]' '{print $2}' > theta.csv
cat  $filename | grep "x" | awk -F '[,:]' '{print $2}' | awk -F '[ ]' '{print $2}' > x.csv
cat $filename | grep "y" | awk -F '[:]' '{print $2}' | awk -F '[ ]' '{print $2}' > y.csv


paste -d, state_id.csv theta.csv  x.csv  y.csv > state_point.csv

rm -f state_id.csv theta.csv x.csv y.csv
echo "complete"