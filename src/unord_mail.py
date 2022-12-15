from decouple import config
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
import smtplib
import ssl



def send_email_with_attachments(sender: str, receivers: list, subject: str, body: str,
                                ccs: list, bccs: list, files: list = []):
    # Create context (to specify TLS version)
    sc = ssl.create_default_context()
    sc.options |= ssl.OP_NO_TLSv1_2 | ssl.OP_NO_TLSv1_3
    sc.minimum_version = ssl.TLSVersion["TLSv1_1"]

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
    server.starttls(context=sc)
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

def main():
    send_test_email(['gore@unord.dk'])


if __name__ == '__main__':
    main()