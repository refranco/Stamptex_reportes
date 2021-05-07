# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 14:50:36 2021

Funciones para generar los reportes de ventas periódigos.
@author: Esteban Franco
"""

def weekly_report(Dataframe):
    from datetime import datetime
    
    today = datetime.now()
    
    if today.isoweekday() == 6:
        print('day time')
    else:
        return
    
    return

def daily_report(ventas_df,date):
    """
    Funcion para reportar las ventas diarias por todas las diferentes entradas que tiene el negocio

    Parameters
    ----------
    ventas_df : TYPE
        DESCRIPTION.
    date : TYPE
        DESCRIPTION.

    Returns
    -------
    reporte_diario : TYPE
        DESCRIPTION.

    """
    import pandas as pd
    
    reporte_diario = pd.DataFrame(data=None, columns=None)
    
    dia_df = ventas_df[ventas_df['Marca temporal'] == date]
    
    total_ventas = dia_df.groupby('Marca temporal').agg({'Valor total venta': 'sum','valor pagado':'sum'})
    reporte_diario['Total vendido'] = total_ventas['Valor total venta']
    reporte_diario['Total pagado'] = total_ventas['valor pagado']
    reporte_diario['Total esperado'] = total_ventas['Valor total venta'] - total_ventas['valor pagado']
    
    num_ventas_local = dia_df['Punto de venta'].value_counts()
    for local in num_ventas_local.index:
        reporte_diario[f'N. Ventas {local}'] = num_ventas_local[local]
        
    tipo_servicio = dia_df.groupby('Servicio 1').agg({'Valor total venta': 'sum'})
    for servicio in tipo_servicio.index:
        reporte_diario[servicio] = tipo_servicio.loc[servicio,'Valor total venta']
        
    por_local = dia_df.groupby('Punto de venta').agg({'Valor total venta': 'sum','valor pagado':'sum'})
    for local in por_local.index:
        reporte_diario[local] = por_local.loc[local,'Valor total venta']
    
    tipo_pago = dia_df.groupby('forma de pago').agg({'Valor total venta': 'sum'})
    
    for forma_pago in tipo_pago.index:
        reporte_diario[forma_pago] = tipo_pago.loc[forma_pago,'Valor total venta']
    
    return reporte_diario

def monthly_report(Dataframe):
    
    import datetime
    import pandas as pd
    import numpy as np
    today = datetime.date.today()
    Dataframe['month'] = Dataframe['Marca temporal'].map(lambda dt: dt.month)
    Dataframe = Dataframe[Dataframe['month'] == today.month]
    # Dataframe['Marca temporal'] = Dataframe['Marca temporal'].map(lambda time: time.date())
    
    Dataframe = Dataframe.sort_values(by='Marca temporal')
    
    dias = Dataframe['Marca temporal'].value_counts().index.sort_values(ascending=True)
    
    reporte_mes = pd.DataFrame(data=None,columns=None)
    for dia in dias:
        diario = daily_report(Dataframe,dia)
        
        reporte_mes = pd.concat([reporte_mes,diario],axis=0)
    reporte_mes.sort_values(by='Marca temporal',ascending=True)
    
    reporte_mes = reporte_mes.fillna(0)
    reporte_mes.loc['TOTAL'] = 0
    for col in reporte_mes.columns:
        reporte_mes.loc['TOTAL',col] = np.sum(reporte_mes[col])
        
    
        
    return reporte_mes
        