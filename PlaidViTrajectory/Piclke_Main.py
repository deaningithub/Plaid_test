# -*- coding: utf-8 -*-

import pickle
import glob
import matplotlib.pyplot as plt
import numpy as np
import os
application = ""
GetPath = 'D:\\Smart_meter\\PLAID\\PickleFile\\'+application+'*.pickle'
PathList = glob.glob(GetPath)
#print(PathList)

SeeStart = 1
SeeLength = 6000

for path in PathList:
    if os.path.getsize(path) > 0:
        with open(path, 'rb') as file:
            Data =pickle.load(file)
            #print(np.shape(Data))
            
            #print(np.max(Data[0]))
            fig1 = plt.figure()
            print(path)
            plt.plot(Data[0],Data[1], 'y-')
           
            plt.show()
        
        
