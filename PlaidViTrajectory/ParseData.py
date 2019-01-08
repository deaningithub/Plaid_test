# -*- coding: utf-8 -*-


#import subprocess
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from datetime import datetime
plt.style.use('ggplot')

from pylab import rcParams
rcParams['figure.figsize'] = (10, 6)

import matplotlib
font = {'family' : 'sans-serif',
        'weight' : 'normal',
        'size'   : 17}
matplotlib.rc('font', **font)

import warnings
warnings.filterwarnings("ignore")



def read_data_given_id(path,ids,progress=True,last_offset=0):
    
    '''read data given a list of ids and CSV paths'''
    start = datetime.now()
    n = len(ids)
    
    if n == 0:
        return {}
    else:
        
        data = {}
        for (i,ist_id) in enumerate(ids, start=1):
            
            if progress and np.mod(i,np.ceil(n/10))==0:
                
                print('%d/%d (%2.0f%s) have been read...\t time consumed: %ds'\
                      %(i,n,i/n*100,'%',(datetime.now()-start).seconds))
            if last_offset==0:
               data[ist_id] = np.genfromtxt(path+str(ist_id)+'.csv',delimiter=',',\
                                         names='current,voltage',dtype=(float,float))
                
            elif ist_id<200:#read every .csv's tail -10000 row, Dean have change to read every row because of the unix not sutable in windows. 
                
#                p=subprocess.Popen(['tail','-'+str(int(last_offset)),path+str(ist_id)+'.csv'],\
#                                   stdout=subprocess.PIPE)
                data[ist_id] = np.genfromtxt(path+str(ist_id)+'.csv',delimiter=',',\
                                         names='current,voltage',dtype=(float,float))
            else:
                pass
        print('%d/%d (%2.0f%s) have been read(Done!) \t time consumed: %ds'\
            %(n,n,100,'%',(datetime.now()-start).seconds)) 
        return data


def clean_meta(ist):
    '''remove None elements in Meta Data ''' 
    clean_ist = ist.copy()
    for k,v in ist.items():
        if len(v) == 0:
            del clean_ist[k]
    return clean_ist
                
def parse_meta(meta):
    '''parse meta data for easy access'''
    M = {}
    for m in meta:
        for app in m:
            M[int(app['id'])] = clean_meta(app['meta'])
#   {
#   'id': '1069', 
#   'meta': 
#         {
#        'header': 
#            {
#            'collection_time': 'July, 2013', 
#            'sampling_frequency': '30000Hz', 
#            'notes': 'some instances are not well calibrated, meta data are not complete'}, 
#        'instances': 
#            {
#            'status': 'off-on', 
#            'length': '2.00s'}, 
#        'type': 'Laptop', 
#        'location': 'house55', 
#        'appliance': 
#            {
#             'manufacture_year': '', 
#             'brand': '', 
#             'voltage': '',
#             'current': '',
#             'wattage': '',
#             'model_number': '',
#             'notes': ''}
#         }
#    }
    return M










Data_path = 'D:\\Smart_meter\\PLAID\\'
csv_path = Data_path + 'CSV\\';

import json
# read meta
with open(Data_path + 'meta1.json') as data_file:    
    meta1 = json.load(data_file)

    
Meta = parse_meta([meta1])
meta1 = parse_meta([meta1])

#print(Meta)
# read data
# applinace types of all instances
Types = [x['type'] for x in Meta.values()]

# unique appliance types
Unq_type = list(set(Types)) # Total 11 types 
Unq_type.sort()
IDs_for_read_data = list(Meta.keys())
#print(IDs_for_read_data )
# households of appliances
Locs = [x['header']['collection_time']+'_'+x['location'] for x in Meta.values()]
# unique households
Unq_loc = list(set(Locs))
Unq_loc.sort()
Origianl_Unq_type = Unq_type

print('Number of households: %d\nNumber of total measurements:%d'%(len(Unq_loc),len(Locs)))


npts = 60000
#print(csv_path)
Data = read_data_given_id(csv_path,IDs_for_read_data,progress=True, last_offset=npts)
print("ReadDone")
#%%
#CTRL + enter 执行当前cell
#
#shift+enter 运行当前cell并将光标移到下一个cell
#print('Total number of instances:',len(Data))


type_Ids = {}
loc_Ids = {}
Mapping = {}
n = len(Data)
print(n)
n = 2890
print(n)
type_label = np.zeros(n,dtype='int')
loc_label = np.zeros(n,dtype='int')
for (ii,t) in enumerate(Unq_type):
    #print(ii,t)
    type_Ids[t] = [i-1 for i,j in enumerate(Types,start=1) if j == t]
    #print(type_Ids[t])
    type_label[type_Ids[t]] = ii
    Mapping[ii] = t
for (ii,t) in enumerate(Unq_loc):
    loc_Ids[t] = [i-1 for i,j in enumerate(Locs,start=1) if j == t]
    loc_label[loc_Ids[t]] = ii+1
print('number of different types: %d'% len(Unq_type))
print('number of different households: %d'% len(Unq_loc))


#%%
fs = 30000
f0 = 60
NS = int(fs/f0) # number of samples per period
NP = int(npts/NS) # number of periods for npts

# calculate the representative one period of steady state 
# (mean of the aggregated signals over one cycle)
n = len(Data)
rep_I = np.empty([n,NS])
rep_V = np.empty([n,NS])
for i in range(n):
    ind = list(Data)[i]
    tempI = np.sum(np.reshape(Data[ind]['current'],[NP,NS]),0)/NP
    tempV = np.sum(np.reshape(Data[ind]['voltage'],[NP,NS]),0)/NP
    # align current to make all samples start from 0 and goes up
    ix = np.argsort(np.abs(tempI))
    j = 0
    while True:
        if ix[j]<499 and tempI[ix[j]+1]>tempI[ix[j]]:
            real_ix = ix[j]
            break
        else:
            j += 1
    rep_I[i,] = np.hstack([tempI[real_ix:],tempI[:real_ix]])
    rep_V[i,] = np.hstack([tempV[real_ix:],tempV[:real_ix]])
    rep_I[i,] = rep_I[i,] / max(rep_I[i,])
    rep_V[i,] = rep_V[i,] / max(rep_V[i,])
    
f1 = np.hstack([rep_I, rep_V])