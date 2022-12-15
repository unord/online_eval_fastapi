from decouple import config
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
import smtplib
import ssl

#from mailer import Mailer
#from mailer import Message



def send_email_with_attachments(sender: str, receivers: list, subject: str, body: str,
                                ccs: list, bccs: list, files: list = []):

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ', '.join(receivers)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    if files is not None:
        for file in files:
            with open(file, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(file)
                )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
            msg.attach(part)
    if ccs is not None:
        msg['Cc'] = ', '.join(ccs)
    if bccs is not None:
        msg['Bcc'] = ', '.join(bccs)
    receivers = receivers + ccs + bccs
    server = smtplib.SMTP('smtp.efif.dk', 25)
    # creating the SMTP server object by giving SMPT server address and port number
    server.ehlo()  # setting the ESMTP protocol
    server.starttls()  # setting up to TLS connection
    server.ehlo()  # calling the ehlo() again as encryption happens on calling startttls()
    server.login(config('EMAIL_USER'), config('EMAIL_PASSWORD'))
    text = msg.as_string()
    server.sendmail(sender,  receivers, text)
    server.quit()


def send_test_email(reciver_list: list):
    send_email_with_attachments(
        'ubot@unord.dk',
        reciver_list,
        'Online-Eval-FastApi Test',
        'This is a test email from Online-Eval-FastApi',
        [],
        [],
        []
    )

'''
def send_email_with_attachments_with_mailer(sender: str, receivers: list, subject: str, body: str, ccs: list, bccs: list, files: list = []):
    message = Message(From=sender, To=receivers,  Subject=subject, charset="utf-8")
    if ccs is not None:
        message.cc = ccs
    if bccs is not None:
        message.bcc = bccs
    message.Body = body
    if files is not None:
        for file in files:
            message.attach(file)
    mailer = Mailer('smtp.efif.dk', port=25)
    #mailer.starttls()
    mailer.login(config('EMAIL_USER'), pwd=config('EMAIL_PASSWORD'))
    mailer.send(message)
'''

def main():
    send_test_email(['gore@unord.dk'])


if __name__ == '__main__':
    main()