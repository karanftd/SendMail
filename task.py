from flask import Flask
import smtplib
from email import MIMEMultipart
from email import MIMEText
from email import MIMEBase
from email import encoders
from celery import Celery
from celery.utils.log import get_logger
from settings import *


app = Flask(__name__)
logger = get_logger(__name__)


'''
get setting from settings.py
'''
#app.config.from_object(settings)

#redisobj = redis.StrictRedis(host='localhost', port=6379, db=0)
celery = Celery(app.import_name, broker=CELERY_BROKER_URL)
celery.conf.update(app.config)



@celery.task(name="send_mail")
def sendMail(from_addr, to_addr_dict, subject, mail_body, send_mail_server, ps, send_mail_port=587, send_file_name_as=None, send_file_path=None ):
    
    """
    simple send mail with body and attachment
    :param from_addr: str|sender email address
    :param to_addr_dict: dict of list of str| list of receiver email address
    :param subject: str| subject of email
    :param mail_body: str|email body
    :param send_mail_server: str|
    :param ps: str| password
    :param send_mail_port: int|
    :param send_file_name_as: str|filename of the attachment
    :param send_file_path: str|path to the attachment
    """
    
    logger.info("sending mail activity started")

    try:
        msg = MIMEMultipart.MIMEMultipart()
        msg['From'] = from_addr

        msg['To'] = ", ".join(to_addr_dict["To"])
        msg['CC'] = ", ".join(to_addr_dict["CC"])
        msg['BCC'] = ", ".join(to_addr_dict["BCC"])

        msg['Subject'] = subject

        msg.attach(MIMEText.MIMEText(mail_body, 'plain'))

        #TODO : Attachment for mail
        '''
        if send_file_name_as and send_file_path:
            attachment = open(send_file_path, "rb")
        part = MIMEBase.MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % send_file_name_as)
        msg.attach(part)
        '''

        # Mailing server info
        server = smtplib.SMTP(send_mail_server, send_mail_port)
        server.starttls()

        server.login(from_addr, ps)

        text = msg.as_string()

        logger.info("sending email one by one")

        for k in to_addr_dict:
            if to_addr_dict[k]:
                logger.info('sending mail to %r', to_addr_dict[k])
                server.sendmail(from_addr, to_addr_dict[k], text)

        server.quit()
        logger.info("Successfully sent email")

    except Exception, e:
        logger.exception('Error: unable to send email %r', e)

