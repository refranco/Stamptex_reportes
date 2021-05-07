# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 12:31:00 2021

@author: Esteban Franco
"""

import pandas as pd
import itertools
path = r'C:\Users\Estef\Dropbox (Personal)\Textamper\Documentacion_procesos'
file = 'Lista_productos_y_atributos.xlsx'

# productos = ['CAMISETA']
productos = ['CAMISETA','GORRA','CHOMPA','MUG','TERMO','CAMISA','CAMIBUSO',
              'CHALECO','TAPABOCAS','PANTALON','UNIFORME','OVEROL','DELANTAL',
              'BOLSA ECOLÓGICA','MAMELUCO','VINILO','TRANSFER']

writer = pd.ExcelWriter(f'{path}/productos_inventario_siigo.xlsx', engine='xlsxwriter')
for producto in productos:
    # llamar los atributos de cada producto
    file_producto = pd.read_excel(f'{path}/{file}',sheet_name=producto)
    # crear lista donde se guardan las combinaciones unicas
    unique_combinations = [ ]
    for col in file_producto.columns:
        atributos = [x for x in file_producto[col].values if isinstance(x,str)]
        unique_combinations.append(atributos)
    
    combinations = list(itertools.product(*unique_combinations))
    lista_productos = []
    for combination in combinations:
        item = producto+' '+', '.join(combination)
        lista_productos.append(item)
    
    df = pd.DataFrame(data=lista_productos,columns=[producto])
    df['PRECIO'] = ''
    df.to_excel(writer, sheet_name=producto,index=False)
    

writer.save()
    
        
