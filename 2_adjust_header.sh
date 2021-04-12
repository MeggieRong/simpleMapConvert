#!/bin/bash


filename=output_files/rest_stations.json

#删除第一行
sed -i '1d' $filename

#给开头部分加入固定内容
sed -i '1i "charge-stations": [' $filename
sed -i '1i "rest-stations": [],' $filename
sed -i '1i {' $filename

#给最后一行加入固定内容 ： }
sed -i '$a}' $filename


echo "complete"