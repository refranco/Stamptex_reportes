# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 06:02:39 2021
STT.aux_functions

Funciones para analizar las ventas de Textamper.
@author: Esteban Franco
"""

#%% MODULOS PARA GENRAR REPORTES.

def resumen_pedidos(df):
    """
    Organiza  la base de datos entregada con la información necesaria para los operarios y el comprador de insumos.
    Los campos a entregar son: Fecha de entrega, Datos cliente, Restante a pagar, Informacion producto 1, 
    Información producto 2, Información producto 3, Información producto 4, Información producto 5,
    Parameters
    ----------
    df : TYPE
        DESCRIPTION.

    Returns
    -------
    Dataframe_resumen : TYPE
        DESCRIPTION.

    """
    import pandas as pd

    ordenes_finales= []
    lista_productos = ['Camiseta','Gorra','Chompa','Termo','Mug','Camisa','Camibuso','Chaleco',
                       'Tapabocas','Pantalon','Uniforme','Overol','Delantal','Bolsa Ecológica''Mamelucos']
    for index in df.index:
        
        orden = {}
        orden['Fecha entrega'] = df.loc[index,'Entrega']
        orden['Datos cliente'] = 'Cliente: {} \n correo: {} \n celular: {}'.format(df.loc[index,'Nombre persona / razón social'],
                                                              df.loc[index,'Correo electrónico'],
                                                              df.loc[index,'celular'])
        
        valor_total_venta = df.loc[index,'Valor total venta']#.replace('.','')
        valor_pagado =df.loc[index,'valor pagado']#.replace('.','')
        orden['Restante a pagar'] = int(valor_total_venta) - int(valor_pagado)
        
        for s in range(1,6):
            if df.loc[index,f'Servicio {s}']:
            
                orden[f'Informacion producto {s}'] = ''
                servicio = df.loc[index,f'Servicio {s}']
                orden[f'Informacion producto {s}'] += f'Servicio: {servicio},'
                # saber si es MAQUILA o PRODUCTO PERSONALIZADOS
                if servicio == 'Solo Maquila':
                    
                    maquila_s_cols = [column for column in df.columns if f'maquila {s}' in column]
                    for atributo in maquila_s_cols:
                        campo = df.loc[index,atributo]
                        if 'Cantidad' in atributo:
                            orden[f'Cantidades producto {s}'] = campo
                        else:
                            orden[f'Informacion producto {s}'] += f'{atributo}: {campo}, '
                else:
                    # PRODUCTO PERSONALIZADO
                    # Saber si es PRODUCTO DE LA LISTA  u OTRO PRODUCTO
                    producto = df.loc[index, f'Producto {s}'].lower()
                    if df.loc[index, f'Producto {s}'] in lista_productos:
                        orden[f'Informacion producto {s}'] += f'Producto personalizado: {producto}, '
                        producto_s_cols = [column for column in df.columns if f'{producto} {s}' in column]
                        for atributo in producto_s_cols:
                            campo = df.loc[index,atributo]
                            orden[f'Informacion producto {s}'] += f'{atributo}: {campo},'
                    else:
                        orden[f'Informacion producto {s}'] += f'Otro producto {s}: {producto},'
                        orden[f'Informacion producto {s}'] += 'Atritubos otro producto {}: {}'.format(s,
                            df.loc[index,f'atributo otro {s}'])
                        
                    caracteristicas_pedido = [column for column in df.columns if f'producto {s}' in column]
                    for atributo in caracteristicas_pedido:
                        campo = df.loc[index,atributo]
                        if 'Cantidad' in atributo:
                            orden[f'Cantidades producto {s}'] = campo
                        else:
                            orden[f'Informacion producto {s}'] += f'{atributo}: {campo},'
                        
                    
                        
        ordenes_finales.append(orden)
    Dataframe_resumen = pd.DataFrame(ordenes_finales)
    return Dataframe_resumen

def proximos_pedidos(df, Ndias_anteriores,Ndias_posteriores):
    
    import datetime
    import pandas as pd
    
    start_date = datetime.datetime.now() - datetime.timedelta(days=Ndias_anteriores)
    end_date = start_date + datetime.timedelta(days=Ndias_anteriores+Ndias_posteriores+1)
    df['Entrega'] = pd.to_datetime(df['Entrega'], dayfirst=True)
    
    prox_pedidos = df['Entrega'] >= start_date
    prox_2_dias = df['Entrega'] < end_date
    filtro_proximos_dias = prox_pedidos & prox_2_dias
    df_prox_dias = df.loc[filtro_proximos_dias]
    df_prox_dias.sort_values(by='Entrega')
    return df_prox_dias


