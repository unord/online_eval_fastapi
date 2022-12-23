from decouple import config
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
import smtplib
import ssl
import time

#from mailer import Mailer
#from mailer import Message



def send_email_with_attachments(sender: str, receivers: list, subject: str, body: str,
                                ccs: list, bccs: list, files: list = []) -> dict:
    # Create a secure SSL context
    context = ssl.create_default_context()

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
    try:
        server = smtplib.SMTP('smtp.efif.dk', 25)
    except Exception as e:
        print(f'Could not connect to smtp server. {e}')
        print("waiting 10 minutes and trying again: server = smtplib.SMTP('smtp.efif.dk', 25)")
        time.sleep(600)
        try:
            server = smtplib.SMTP('smtp.efif.dk', 25)
        except Exception as e:
            print(f'Second attempt: Could not connect to smtp server. {e}')
            print('failed to send email')
            return {'msg': 'Failed to send email', 'success': False}
        server = smtplib.SMTP('smtp.efif.dk', 25)
    server.starttls(ssl_version=ssl.PROTOCOL_TLSv1_3)  # setting up to TLS connection
    server.login(config('EMAIL_USER'), config('EMAIL_PASSWORD'))
    text = msg.as_string()
    try:
        server.sendmail(sender,  receivers, text)
    except Exception as e:
        print(f'Could not connect to smtp server. {e}')
        print('waiting 10 minutes and trying again: server.sendmail(sender,  receivers, text)')
        time.sleep(600)
        try:
            server.sendmail(sender,  receivers, text)
        except Exception as e:
            print(f'Second attempt: Could not connect to smtp server. {e}')
            print('failed to send email')
            return {'msg': 'Failed to send email', 'success': False}
    server.quit()
    return {'msg': 'Email sent', 'success': True}


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