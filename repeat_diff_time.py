import numpy as np
import pandas as pd
file = 'test.csv'
data = pd.read_csv(file,sep=',', names = ['order_num','show_times'])
ll = np.repeat(data.order_num,data.show_times) 
ll = pd.DataFrame(ll)
ll.to_csv('in1v.csv',index = False,header=False)

