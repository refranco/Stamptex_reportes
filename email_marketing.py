# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 18:35:32 2021

@author: Esteban Franco
"""
from STT.email_functions import mail_smtp_setup, email_marketing, read_template
from gsheet_reader import pull_sheet_data
import pandas as pd
#%% main variables
nombre_hoja = 'Hoja 1'
spreadsheet_id = '13y-aUDQjF_97dpKB7fH9H5szxcMSDGvr-1iwZk152i0'

path = r'C:\Users\Estef\Dropbox (Personal)\Textamper\Códigos'

# server setting
Myaddress = 'asistentepedidos.stamptex@gmail.com'
password = 'pedidos.stamptex'
smtp_host = 'smtp.gmail.com'
smtp_port = 587
password = 'pedidos.stamptex'
server = mail_smtp_setup(Myaddress, smtp_host, smtp_port, password)
#%% reading client database

def main():
    data = pull_sheet_data(Cred_name = 'asistentepedidos.json',
                           SCOPES = ['https://www.googleapis.com/auth/spreadsheets'],
                           SPREADSHEET_ID = spreadsheet_id,
                           RANGE_NAME = nombre_hoja)
    clientes = pd.DataFrame(data=data[1:], columns=data[0])


    # Enviar correo a locales
    From = Myaddress
    for index, empresa in enumerate(clientes['NOMBRE EMPRESA EMAIL']):

        nombre =clientes.loc[index,'CONTACTO'].split(' ')[0].title()
        email = clientes.loc[index,'EMAIL']
        To = clientes.loc[index,'EMAIL']
        Subject = f'{nombre}, sabemos que a {empresa} le gusta generar reconocimiento de marca'
        # print(empresa, clientes.loc[index,'CONTACTO'].split(' ')[0].title(),
        #       clientes.loc[index,'EMAIL'], Subject, '\n')
        message = read_template(r'{}\mensaje_publicitario.txt'.format(path))


        message = message.substitute(Nombre=nombre,la_empresa =empresa)

        image_path =  r'C:\Users\Estef\Dropbox (Personal)\Textamper\Marca\logo stamptex email.PNG'
        email_marketing(From,To, Subject,server, message,  image_path=image_path)
    return

if __name__ == '__main__':

    main()

    # este es un comentario de cambio para github
