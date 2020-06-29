import smtplib , ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart





def send_email(args,mail_message):

    sender_email = args.get('mail_sender',"sgp.project.test@gmail.com")
    mail_smtp_server = args.get('mail_smtp_server',"smtp.gmail.com")
    mail_password = args.get('mail_password',"0106231078")
    mail_port = int(args.get('mail_port',587))
    mail_receiver = args.get('mail_receiver',"mfawzy.sami@gmail.com")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = mail_receiver
    msg['Subject'] = "MiniFlow Notification(s)"

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(mail_message, 'plain'))

    server = smtplib.SMTP(mail_smtp_server, mail_port)
    server.ehlo()
    server.starttls()
    server.login(sender_email, mail_password)
    print(msg.as_string())
    server.sendmail(sender_email,[mail_receiver], msg.as_string())
    print ("Email sent To {0}".format(mail_receiver))
    server.close()
