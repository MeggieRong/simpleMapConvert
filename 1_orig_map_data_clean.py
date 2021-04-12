# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import math
import warnings
import csv
import json
warnings.filterwarnings("ignore")

file_path = 'input_files/map.xlsx'

excel_file = pd.read_excel(file_path)
excel_file.x = round(excel_file.x,2)
excel_file.y = round(excel_file.y,2)



#输出投入generateAdjacentList的文件
map = excel_file[['x','y','是否属于货架取放货点']]
map.to_csv('input_files/map.csv', index = False, header = False)


kubot = excel_file[excel_file['类型'] == '充电点'][['x','y']]
kubot['kubot_no'] = list(range(1,len(kubot)+1))
max_y = max(map.y)
min_y = min(map.y)
max_x = max(map.x)
min_x = min(map.x)
kubot['direction'] = list(range(0,len(kubot)))

for i in range(0,len(kubot)):
    if kubot.y.iloc[i] == max_y  and kubot.x.iloc[i] != max_x and kubot.x.iloc[i] != min_x : 
        kubot['direction'].iloc[i] = 1.57
    elif kubot.y.iloc[i] == min_y and kubot.x.iloc[i] != max_x and kubot.x.iloc[i] != min_x: 
        kubot['direction'].iloc[i] = -1.57
    elif kubot.x.iloc[i] == min_x and kubot.y.iloc[i] != max_y and kubot.y.iloc[i] != min_y : 
        kubot['direction'].iloc[i] = -3.14
    else:
        kubot['direction'].iloc[i] = 0


kubot = kubot[['kubot_no','x','y','direction']]
kubot.to_csv('output_files/kubot.csv', index = False, header = False)
kubot.to_csv('output_files/kubot.txt', sep = ',',index = False, header = False)

#station part 
station = excel_file[excel_file['类型'].isin(['工作站入口','工作站出口'])][['类型','x','y']]
station.sort_values(by = ['x','y'],inplace = True,ascending = True)
station_entrance = station[station['类型'] == '工作站入口']
station_entrance['stationId'] = range(1,len(station_entrance)+1)
station_export = station[station['类型'] == '工作站出口']
station_export['stationId'] = range(1,len(station_export)+1)
station = pd.merge(station_entrance,station_export,how ='left', on = 'stationId')
station.dropna(how = 'any', inplace = True)
colNameDict = {
        '类型_x':'station_entrace',
        '类型_y':'station_export',
        'x_x':'x_entrace',
        'y_x':'y_entrace',
        'x_y':'x_export',
        'y_y':'y_export'
}
station.rename(columns = colNameDict,inplace=True)

del station['station_entrace']
del station['station_export']
col = ['stationId','x_entrace','y_entrace','x_entrace','y_entrace','x_export','y_export','x_export','y_export']
col_output_files = ['stationId','x_entrace','y_entrace','x_export','y_export']
station[col].to_csv('output_files/station.csv',index = False, header = False)
station[col_output_files].to_csv('output_files/station_output_files.csv',index = False, header = False)


csvfile = open('output_files/kubot.csv','r')
jsonfile = open('output_files/rest_stations.json','w')
fieldnames = ('kubot id','x','y','theta')
reader = csv.DictReader( csvfile, fieldnames)
            
s = []
for row in reader:
    row['x'] = float(row['x'])
    row['y'] = float(row['y'])
    row['theta'] = float(row['theta'])
    row['kubot id'] = int(row['kubot id'])
    xytheta = ['x', 'y','theta']
    kubot_id = -1
    subdict=dict([(key, row[key]) for key in xytheta])
    position={'position':{}}
    position['position'] = subdict
    concat = {'position':{},'kubotId':{}}
    concat['position'] = subdict
    concat['kubotId']= -1
    s.append(concat)
json.dump(s,jsonfile,indent=1)
jsonfile.write('\n')


print("")
print("Program complete!")