# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 11:59:46 2021
envio de emails
@author: Esteban Franco
"""

#%% MODULO PARA ENVIO DE EMAILS

def read_template(filename):
    """ Function that open a template message kept in path and deliver it as 
    a template"""
    from string import Template
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def mail_smtp_setup(Myaddress, smtp_host,smtp_port, password= None, fh = None):
    """ configurar un puerto stmp para enviar emails"""
    import getpass
    import smtplib, ssl
    import logging
    
    if fh:
        mail_setup = logging.getLogger('mail_setup')
        mail_setup.setLevel(logging.INFO)
        mail_setup.addHandler(fh)
    # starting the SMTP server
    context = ssl.create_default_context()
    server = smtplib.SMTP(host=smtp_host, port=smtp_port) # otherwise 465
    if not password:
        password =getpass.getpass(prompt='Escriba la clave de su correo y presione enter: ',
                                  stream=None)
    
    # setting up the SMTP server  
    server.starttls(context=context)
    server.login(Myaddress,password)
    if fh:
        mail_setup.info('Servidor {} correctamente cargado de la cuenta {}'.format(smtp_host,Myaddress))
    else:
        print('Servidor {} correctamente cargado de la cuenta {}'.format(smtp_host,Myaddress))
    return server

def create_email_message(From,To, Subject,server, message, filename=None,
                         path_attachment=None, fh=None):
    """ Crear un meail para enviar a un usuario en específico con un archivo expecífico
    como template y con un archivo adjunto.
    
    INTPUT
    From: String, recipient email address
    To:   String, My email address
    Subject: String, email subject
    server: SMTP server, configured in function mail_smtp_setup
    message: txt file, message template html style with the substitution of the
                    required fields.
    filename: string, name of the filename with the extension at the end. if None
                there is not file to send
    path_attachment: path to find the attached file
    fh: logging.FileHandler, a handler from the logging library that contains the
            logging leve, the log filename and the format of the message for
            debugging or register.
    """
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import logging
    
    if fh:
        logger_mail = logging.getLogger('mail_message')
        logger_mail.setLevel(logging.INFO)
        logger_mail.addHandler(fh)  #definido en el script principal
    
    msg = MIMEMultipart()       # create a message
    # setup the parameters of the message
    msg['From']= From
    msg['To']= To
    msg['Subject']=Subject
    # add in the message body
    msg.attach(MIMEText(message, 'html'))

    if filename != None:
        # Open PDF file in binary mode
        with open('{}/{}'.format(path_attachment,filename), "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=filename)
        # Add attachment to message 
        msg.attach(part)
        
    # convert message to string
    text = msg.as_string()
    
    # send the message via the server set up earlier.
    try:
        server.sendmail(From, To, text)
        if fh:
            logger_mail.info('enviando email a {}'.format(To))
    except:
        if fh: 
            logger_mail.warning('No se encontro cuenta de email en este index')
   
    del msg
    
    return

def email_marketing(From,To, Subject,server, message, path_attachment=None,
                         filename=None, image_path=None, fh=None):
    """ Crear un meail para enviar clientes con un diseño del email generado en html
     {contenido en message} y con el logo de la empresa. 
    
    INTPUT
    From: String, recipient email address
    To:   String, My email address
    Subject: String, email subject
    server: SMTP server, configured in function mail_smtp_setup
    message: txt file, message template html style with the substitution of the
                    required fields.
    filename: string, name of the filename with the extension at the end. if None
                there is not file to send
    path_attachment: path to find the attached file
    image_path: path to the image


    """
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    import logging
    import mimetypes
    
    if fh:
        logger_mail = logging.getLogger('mail_message')
        logger_mail.setLevel(logging.INFO)
        logger_mail.addHandler(fh)  #definido en el script principal
    
    msg = MIMEMultipart('related')       # create a message
    # setup the parameters of the message
    msg['From']= From
    msg['To']= To
    msg['Subject']=Subject
    
    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)
    
    # texto alternativo, por si el receptor no puede recibir mensajes multimedia
    msgText = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgText)
    # add in the message body in html which contains the image
    msgText = MIMEText(message, 'html')
    msgAlternative.attach(msgText)
    
    if image_path:
        # attaching the image
        fp = open(image_path, 'rb')
        msgImage = MIMEImage(fp.read())
        
        fp.close()
        
        # msgText = MIMEText(message, 'html')
        # Define the image's ID as referenced above
        msgImage.add_header('Content-ID', 'image1')
        # msgImage.set_payload('Content-ID', 'image1')
        msg.attach(msgImage)

    if filename != None:
        # Open PDF file in binary mode
        with open('{}/{}'.format(path_attachment,filename), "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=filename)
        # Add attachment to message 
        msg.attach(part)
        
    # convert message to string
    text = msg.as_string()
    
    # send the message via the server set up earlier.
    try:
        server.sendmail(From, To, text)
        print(f'Sending meail to {To}')
        if fh:
            logger_mail.info('enviando email a {}'.format(To))
    except:
        if fh: 
            logger_mail.warning('No se encontro cuenta de email en este index')
   
    del msg
    
    return