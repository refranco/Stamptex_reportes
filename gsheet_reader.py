# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 11:42:02 2021
Versión modificada de Quickstart.py de google para obtener las credenciales para 

Para configurar la lectura desde otra cuenta o desde otro computador.
Seguir los pasos de:
https://towardsdatascience.com/how-to-import-google-sheets-data-into-a-pandas-dataframe-using-googles-api-v4-2020-f50e84ea4530

La pagina de activación en la cuenta de google y generación del token es
https://developers.google.com/sheets/api/quickstart/python
@author: Esteban Franco
"""
def gsheet_api_check(Cred_name = None,
                     SCOPES = ['https://www.googleapis.com/auth/spreadsheets']):
    """
    Función para chequear las credenciales de una cuenta de google en particular que
    esta guardada en el archivo json {Cred_name}
    
    Cred_name string, nombre del archivo json. i.e. credentials.json
    SCOPES, por defecto será: ['https://www.googleapis.com/auth/spreadsheets']
    """
    import pickle
    import os.path
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                Cred_name, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def pull_sheet_data(Cred_name,SCOPES,SPREADSHEET_ID,RANGE_NAME):
    """Funcion para cargar una googleshet en una lista
    de python"""
    from googleapiclient.discovery import build
    creds = gsheet_api_check(Cred_name,SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME).execute()
    values = result.get('values', [])
    
    if not values:
        print('No data found.')
    else:
        rows = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                  range=RANGE_NAME).execute()
        data = rows.get('values')
        print("COMPLETE: Data copied from {} {}".format(RANGE_NAME,Cred_name[:-5]))
        return data
    return