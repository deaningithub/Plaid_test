# -*- coding: utf-8 -*-
from datetime import datetime
import numpy as np
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
                
#            elif ist_id<200:#read every .csv's tail -10000 row, Dean have change to read every row because of the unix not sutable in windows. 
#                
##                p=subprocess.Popen(['tail','-'+str(int(last_offset)),path+str(ist_id)+'.csv'],\
##                                   stdout=subprocess.PIPE)
#                data[ist_id] = np.genfromtxt(path+str(ist_id)+'.csv',delimiter=',',\
#                                         names='current,voltage',dtype=(float,float))
            else:
                pass
        print('%d/%d (%2.0f%s) have been read(Done!) \t time consumed: %ds'\
            %(n,n,100,'%',(datetime.now()-start).seconds)) 
        return data
    
def read_A_data_by_id(path,ids,progress=True):
    
    start = datetime.now()

    #print('time start:',(datetime.now()-start).seconds)
       
    data = np.genfromtxt(path+str(ids)+'.csv',delimiter=',',\
                             names='current,voltage',dtype=(float,float))
 
 
    #print('time done:',(datetime.now()-start).seconds) 
    return data

