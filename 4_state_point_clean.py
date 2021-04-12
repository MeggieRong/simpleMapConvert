# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import math
import warnings
import csv
import json
warnings.filterwarnings("ignore")


#导入state_point文件
state_point = pd.read_csv('state_point.csv',names = ['state_id','theta','x','y'])
state_point['theta'] = round(state_point['theta'],2)




#导入操作台出入口
station_for_simulation_config = pd.read_csv('station_temp.csv',names = ['station_no','x','y','x_export','y_export'])


#设置操作台配置
print("")
station_type = input('Please choose station type: Normal or Conveyor_JD\n')
print("")
slot_num = int(input('please input the number of slots: '))
print("")
print("Left to Right: 0.00\nRight to Left: -3.14\nUp to Down: -1.57\nDown to Up: 1.57")
station_for_simulation_config['theta'] = input("Please choose the direction when kubot go through station: \n")
station_for_simulation_config['theta'] = station_for_simulation_config['theta'].astype('float64')

#当选择的是Normal操作台
#根据 theta，x ，y三个链接作为一个唯一key值，去state_point匹配得到state_id


if station_type == 'Normal' or station_type == 'normal':
    state_point['key'] = state_point.theta.astype('str')\
                        + state_point.x.astype('str') \
                        + state_point.y.astype('str')
    state_point = state_point[['key','state_id']]
    station_for_simulation_config['key'] = station_for_simulation_config.theta.astype('str')\
                                           + station_for_simulation_config.x.astype('str')\
                                           + station_for_simulation_config.y.astype('str')
    station_for_simulation_config = pd.merge(station_for_simulation_config,state_point, how = 'left', on = ['key'])

    station_for_simulation_config.drop(columns = ['key'],inplace = True)
    station_for_simulation_config.dropna(how='any',inplace=True)
    station_for_simulation_config['state_id'] = station_for_simulation_config['state_id'].astype('int')
else:
    state_point['key'] = state_point.theta.astype('str') \
                         + state_point.x.astype('str')\
                         + state_point.y.astype('str')
    state_point['key_export'] = state_point.theta.astype('str') \
                                + state_point.x.astype('str') \
                                + state_point.y.astype('str')
    state_point = state_point[['key','key_export','state_id']]
    station_for_simulation_config['key'] = station_for_simulation_config.theta.astype('str')\
                                           + station_for_simulation_config.x.astype('str')\
                                           + station_for_simulation_config.y.astype('str')
    station_for_simulation_config['key_export'] = station_for_simulation_config.theta.astype('str') \
                                                  + station_for_simulation_config.x_export.astype('str')\
                                                  + station_for_simulation_config.y_export.astype('str')
    station_for_simulation_config = pd.merge(station_for_simulation_config,state_point, how = 'left', on = ['key'])
    station_for_simulation_config.drop(columns = ['key','key_export_y'],inplace = True)
    station_for_simulation_config.rename(columns = {'key_export_x':'key_export','state_id':'unload_state_id'},inplace = True)
    station_for_simulation_config = pd.merge(station_for_simulation_config,state_point, how = 'left', on = ['key_export'])
    station_for_simulation_config.drop(columns = ['key','key_export'],inplace = True)
    station_for_simulation_config.rename(columns = {'state_id':'load_state_id'},inplace = True)

    station_for_simulation_config.dropna(how='any',inplace=True)
    station_for_simulation_config['unload_state_id'] = station_for_simulation_config['unload_state_id'].astype('int')
    station_for_simulation_config['load_state_id'] = station_for_simulation_config['load_state_id'].astype('int')

station_for_simulation_config.to_csv('station_brief.csv', index = False, header = False)


#将操作台各配置信息及匹配上的state_id处理为符合模拟器使用的json格式
station_csv_file = open('station_brief.csv','r')
jsonfile_station = open('output_files/station_config.json','w')


if station_type == 'Normal' or station_type == 'normal':
    fieldnames_station = ('station id','x','y','export_x','export_y','theta','state_id')
else:
    fieldnames_station = ('station id','x','y','export_x','export_y','theta','unload_state_id','load_state_id')

reader_station = csv.DictReader(station_csv_file,fieldnames_station)


#station_config
k= []
for row in reader_station:
    row['station id'] = int(float(row['station id']))
    row['type'] = station_type
    row['x'] = float(row['x'])
    row['single_item_order_slot_limit'] = 0
    row['single_item_order_only'] = False
    row['y'] = float(row['y'])
    xy = ['x','y']
    subdict=dict([(key, row[key]) for key in xy])
    location={'location':{}}
    location['location'] = subdict


    if station_type == 'Normal' or station_type == 'normal':
        concat = {'station id':{}, \
                  'type':{}, \
                  'location':{}, \
                  'order slot number':{}, \
                  'single-item order slot limit':{}, \
                  'single-item order only':{}, \
                  'target state id':{}}
        concat['station id'] = row['station id']
        concat['type']= row['type']
        concat['location'] = subdict
        concat['order slot number'] = slot_num
        concat['single-item order slot limit'] = 0
        concat['single-item order only'] = False
        concat['target state id'] = int(row['state_id'])
        k.append(concat)
    else:
        concat = {'station id':{}, \
                  'type':{}, \
                  'location':{}, \
                  'order slot number':{}, \
                  'single-item order slot limit':{}, \
                  'single-item order only':{}, \
                  'load state id':{}, \
                  'unload state id':{}}

        concat['station id'] = row['station id']
        concat['type']= row['type']
        concat['location'] = subdict
        concat['order slot number'] = slot_num
        concat['single-item order slot limit'] = 0
        concat['single-item order only'] = False
        concat['unload state id'] = int(row['unload_state_id'])
        concat['load state id'] = int(row['load_state_id'])
        k.append(concat)

json.dump(k,jsonfile_station,indent=1)
jsonfile_station.write('\n')
print('Program completed!')
