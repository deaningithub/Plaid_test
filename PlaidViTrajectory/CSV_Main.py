# -*- coding: utf-8 -*-

import numpy as np
from package import MetaProcess,DatasetProcess
import matplotlib.pyplot as plt

Data_path = 'D:\\Smart_meter\\PLAID\\'
csv_path = Data_path + 'CSV\\';

import json
# read meta
with open(Data_path + 'meta1.json') as data_file:    
    meta1 = json.load(data_file)

    
Meta = MetaProcess.parse_meta([meta1])# Meta is Dict type
meta1 = MetaProcess.parse_meta([meta1])

#print(Meta[1])
# read data
# applinace types of all instances
Types = [x['type'] for x in Meta.values()]

# unique appliance types
Unq_type = list(set(Types)) # Total 11 types 
Unq_type.sort()
IDs_for_read_data = list(Meta.keys())
#IDs_for_read_data = list(range(145,146))
#print(IDs_for_read_data)
#print(IDs_for_read_data )
# households of appliances
Locs = [x['header']['collection_time']+'_'+x['location'] for x in Meta.values()]
# unique households
Unq_loc = list(set(Locs))
Unq_loc.sort()
Origianl_Unq_type = Unq_type

print('Number of households: %d\nNumber of total measurements:%d'%(len(Unq_loc),len(Locs)))


npts = 0
#print(csv_path)
kk = [x['header']['collection_time'] for x in Meta.values()]
print(Meta[5]['type'])
#%%
import pickle
SeeStart = 1
SeeLength = 6000
_period = -500

PkPath = 'D:\\Smart_meter\\PLAID\\PickleFile\\'

for i in IDs_for_read_data:
    path = PkPath+Meta[i]['type']+str(i)+'.pickle'
    picklefile = open(path, 'wb')
    
#    if Meta[i]['type'] == "Fan":
#        #print(i,Meta[])
#        Data = DatasetProcess.read_A_data_by_id(csv_path,i,progress=True)
#        #Data = DatasetProcess.read_data_given_id(csv_path,IDs_for_read_data,progress=True, last_offset=npts)
#        print(Meta[i]['type'],'id=',i)
#        #print(Data['current'])
#    
#        fig1 = plt.figure()
#        Data2 = Data['current'] - np.roll(Data['current'],_period)
#    #    plt.plot(Data['current'],Data['voltage'], 'r-')
#        plt.plot(Data['voltage'][SeeStart:SeeLength+SeeStart]/300, 'b-')
#        plt.plot(Data['current'][SeeStart:SeeLength+SeeStart], 'r-')
#        #plt.plot(Data2[SeeStart:SeeLength+SeeStart],Data['voltage'][SeeStart:SeeLength+SeeStart], 'y-')
#       
#        plt.show()
    #print(i,Meta[])
    Data = DatasetProcess.read_A_data_by_id(csv_path,i,progress=True)
    #print(np.shape(Data))
    #Data = DatasetProcess.read_data_given_id(csv_path,IDs_for_read_data,progress=True, last_offset=npts)
    DataC= Data['current'] - np.roll(Data['current'],_period)
    DataS = np.empty(len(DataC)*2)
    DataS.resize(2,len(DataC))
    DataS_counter = 0
    for j in range(len(DataC)):
        if np.abs(DataC[j]) > 0.4:
            DataS[0][DataS_counter],DataS[1][DataS_counter] = DataC[j],Data['voltage'][j]
           
            DataS_counter += 1
    print(len(DataC),np.shape(DataS),DataS_counter)
    #DataS = DataS[0:DataS_counter]
    DataK = np.empty(DataS_counter*2)
    DataK.resize(2,DataS_counter)
    DataK[0] = DataS[0][0:DataS_counter]
    DataK[1] = DataS[1][0:DataS_counter]
    print(np.shape(DataK))
    DataS = DataK
    
    #DataV = Data['voltage'][0:len(DataC)]
    #DataS = [DataC,Data['voltage'][0:len(DataC)]]
    

            #DataS = [DataC[i],Data['voltage'][i]]
    
    #print(np.shape(Data))
    print(Meta[i]['type'],'id=',i)
    pickle.dump(DataS, picklefile)
    picklefile.close()
    #print(Data['current'])
    print(np.shape(DataS))
    fig1 = plt.figure()
    SeeLength = DataS_counter
#    plt.plot(Data['current'],Data['voltage'], 'r-')
    #plt.plot(Data['voltage'][SeeStart:SeeLength+SeeStart]/150, 'b-')
    #plt.plot(Data['current'][SeeStart:SeeLength+SeeStart], 'r-')
    plt.plot(DataS[0][SeeStart:SeeLength+SeeStart],DataS[1][SeeStart:SeeLength+SeeStart], 'y-')
   
    plt.show()
    picklefile.close()
