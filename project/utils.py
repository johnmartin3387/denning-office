import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header

def send_email(user, pwd, sender, recipient, subject, body):
    gmail_user = user
    gmail_pwd = pwd
    FROM = sender
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = MIMEText(body, 'html')

    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = formataddr((str(Header('Denning IT', 'utf-8')), 'from@mywebsite.com'))
    msg['To'] = ", ".join(TO)

    msg.attach(TEXT)

    if True: #try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, msg.as_string())
        server.close()
        print 'successfully sent the mail:\n'
        return True
    #except:
    #    print "failed to send mail:\n"
    #    return False