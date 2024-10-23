import smtplib
import email.mime.multipart
import email.mime.base
import os
from email.mime.text import MIMEText
import datetime

fecha_actual = datetime.datetime.now()
# Formatear la fecha en el formato _YYYYMMDD
fecha_desglosada = fecha_actual.strftime("%Y%m%d")

remitente = 'aemirandagarcia@gmail.com'
destinatario = 'aemirandagarcia@gmail.com'

server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login('aemirandagarcia@gmail.com','ivnh hanr sydh dakn')


mensaje = email.mime.multipart.MIMEMultipart()
mensaje['From'] = remitente
mensaje['To'] = destinatario
mensaje['Subject'] = "Reporte Asistencia_" + fecha_desglosada

cuerpo = "Envio de reporte de asistencia_" + fecha_desglosada
mensaje.attach(email.mime.text.MIMEText(cuerpo, 'plain'))

ruta_Archivo = 'Reporte_asistencia_' + fecha_desglosada + '.xlsx'
archivo = open(ruta_Archivo, 'rb')
adjunto = email.mime.base.MIMEBase('application','octet-stream')
adjunto.set_payload((archivo).read())
email.encoders.encode_base64(adjunto)
adjunto.add_header('Content-Disposition', "attachment; filename= %s" %ruta_Archivo)
mensaje.attach(adjunto)
texto = mensaje.as_string()


server.sendmail(remitente, destinatario, texto)
server.quit()