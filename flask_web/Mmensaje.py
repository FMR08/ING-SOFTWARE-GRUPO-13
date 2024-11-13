import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

nombre = input("Por favor, ingresa tu nombre: ")
especialista = input("Por favor, ingresa tu nombre: ")

remitente = 'correoaaa999@gmail.com'
password = 'gwjy txfu mozm lnmk'  #password$$220

# despues pedir correo (destinatario = input("Por favor, ingresa el correo del destinatario: "))
destinatario = 'correoaaa999@gmail.com'

Asunto = 'Confirmación de Reserva'
body =( 'Hola, señor/señora ' + nombre + 
    ',\nle escribibimos para confirmar su resebacion con '
    +especialista + 'Clic aqui: http://localhost:5000/confirmar_visita'
    
)

# Crear el mensaje MIME
mensaje = MIMEMultipart()
mensaje['From'] = remitente
mensaje['To'] = destinatario
mensaje['Subject'] = Asunto
mensaje.attach(MIMEText(body, 'plain'))



server = smtplib.SMTP_SSL('smtp.gmail.com' )
server.login(remitente, password) 
text = mensaje.as_string()
server.sendmail(remitente, destinatario, text)
server.quit()  
