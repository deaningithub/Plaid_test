# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 09:17:14 2018

@author: lstDe
"""
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


