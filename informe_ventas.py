# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 12:22:47 2021

scrip para generar informe general de Ventas STampTeX

@author: Esteban Franco
"""
from gsheet_reader import pull_sheet_data
from STT.querys_functions import resumen_pedidos,proximos_pedidos 
from STT.email_functions import mail_smtp_setup, create_email_message, read_template
from STT.ventas_functions import daily_report, monthly_report
import pandas as pd
import os
import datetime
import numpy as np
path = os.getcwd()


nombre_hoja = 'pedidos ventanilla'
spreadsheet_id = '1x5y7wUpVS3ApXfTdmmauRQcQ3SaRMPCsflQE47-NGsg'


data = pull_sheet_data(Cred_name = 'asistentepedidos.json',
                       SCOPES = ['https://www.googleapis.com/auth/spreadsheets'],
                       SPREADSHEET_ID = spreadsheet_id,
                       RANGE_NAME = nombre_hoja)

form_pedidos = pd.DataFrame(data=data[1:], columns=data[0])

# cambiando las columnas que tienen datos de tiempo a columnas tipo datetime.
form_pedidos['Marca temporal'] = pd.to_datetime(form_pedidos['Marca temporal'], dayfirst=True)
form_pedidos['Entrega'] = pd.to_datetime(form_pedidos['Entrega'], dayfirst=True)

form_pedidos['Valor total venta'] = form_pedidos['Valor total venta'].map(lambda st: int(st.replace('.','')))
form_pedidos['valor pagado'] = form_pedidos['valor pagado'].map(lambda st: int(st.replace('.','')))

#%% Generar cronograma de próximos pedidos.
def main():
    # recopilar los pedidos de los siguientes dias (2 próximos dias y el dia anterior)
    DataFrame_prox_dias = proximos_pedidos(form_pedidos, 2,4)
    
    # filtrar pedidos por locales
    pedidos_laureles = DataFrame_prox_dias[DataFrame_prox_dias['Punto de venta'] == 'Laureles']
    pedidos_aranjuez = DataFrame_prox_dias[DataFrame_prox_dias['Punto de venta'] == 'Aranjuez']
    
    # Resumen de pedidos de cada logal
    proximos_laureles = resumen_pedidos(pedidos_laureles)
    proximos_laureles = proximos_laureles.sort_values(by='Fecha entrega',ascending=True)
    proximos_laureles.to_excel('proximos_laureles.xlsx',index=False)
    
    proximos_aranjuez = resumen_pedidos(pedidos_aranjuez)
    proximos_aranjuez = proximos_aranjuez.sort_values(by='Fecha entrega',ascending=True)
    proximos_aranjuez.to_excel('proximos_aranjuez.xlsx',index=False)
    
    # resumen de pedidos para compras
    writer = pd.ExcelWriter('Pedidos_proximos_dias.xlsx', engine='xlsxwriter')
    proximos_aranjuez.to_excel(writer, sheet_name='Aranjuez', index=False)
    proximos_laureles.to_excel(writer,sheet_name='Laureles', index=False)
    writer.save()
    # ---------- ENVIAR RESUMEN  DE PEDIDOS A LOCALES -------------------------
    
    # configurar servidor
    Myaddress = 'asistentepedidos.stamptex@gmail.com'
    password = 'pedidos.stamptex'
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    password = 'pedidos.stamptex'
    server = mail_smtp_setup(Myaddress, smtp_host, smtp_port, password)
    
    # Enviar correo a locales
    From = Myaddress
    To = 'pedidos.laureles@gmail.com'
    Subject = 'Pedidos de hoy y próximos dias Laureles'
    message = read_template(r'{}\resumen_locales.txt'.format(path))
    local = 'Laureles'
    tabla_laureles =  proximos_laureles.to_html()
    template_message = message.substitute(Nombre = local, tabla = tabla_laureles)
    
    create_email_message(From,To, Subject,server, template_message, filename='proximos_laureles.xlsx', 
                          path_attachment=path, fh=None)
    
    From = Myaddress
    To = 'pedidos.aranjuez1@gmail.com'
    Subject = 'Pedidos de hoy y próximos dias Aranjuez'
    message = read_template(r'{}\resumen_locales.txt'.format(path))
    local = 'Aranjuez'
    tabla_aranjuez =  proximos_aranjuez.to_html()
    template_message = message.substitute(Nombre = local, tabla = tabla_aranjuez)
    
    create_email_message(From,To, Subject,server, template_message, filename='proximos_aranjuez.xlsx', 
                          path_attachment=path, fh=None)
    
    # ------ENVIAR RESUMEN DE COMPRAS AL AREA DE INSUMOS
    From = Myaddress
    To = 'chjessua@gmail.com'
    Subject = 'Pedidos de hoy y próximos dias STAMPTEX'
    message = read_template(r'{}\resumen_materiales.txt'.format(path))
    nombre = 'Cristian'
    
    template_message = message.substitute(Nombre = nombre, Taranjuez = tabla_aranjuez,
                                          Tlaureles = tabla_laureles)
    
    create_email_message(From,To, Subject,server, template_message, filename='Pedidos_proximos_dias.xlsx', 
                          path_attachment=path, fh=None)


#%% ANALISIS  FINANCIERO
    
    ventas_df = pd.concat([form_pedidos.iloc[:, 0:4],form_pedidos.iloc[:,-9:]], axis=1)
    ventas_df['Marca temporal'] = pd.to_datetime(ventas_df['Marca temporal'], dayfirst=True)
    ventas_df['Marca temporal'] = ventas_df['Marca temporal'].map(lambda dt: dt.date())
    ventas_df['Valor total venta'] = pd.to_numeric(ventas_df['Valor total venta'])
    ventas_df['valor pagado'] = pd.to_numeric(ventas_df['valor pagado'])
    dia_reporte = datetime.date.today() - datetime.timedelta(days=0)
    
    dia = daily_report(ventas_df,dia_reporte)
    
    reporte_mes = monthly_report(ventas_df)
    
    writer = pd.ExcelWriter('reporte_mes.xlsx', engine='xlsxwriter')
    
    reporte_mes.to_excel(writer,sheet_name='Reporte mes')
    dia.to_excel(writer,sheet_name=str(dia_reporte))
    writer.save()
    
    return
    
if __name__ == '__main__':
    
    main()

