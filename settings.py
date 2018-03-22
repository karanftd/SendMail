SMTP_USER_NAME = 'EmailAddress'
SMTP_PASSWORD = 'Password'

#send mail to
'''
to_address_dict = {"To":["receiver@example.com"],
                   "CC":["cc@example.com"],
                   "BCC":["bcc@example.com"]}


#subject
subject = "Test mail from python script"

#body
mail_body = "MAIL BODY\n" \
            "MAIL BODY\n" \
            "MAIL BODY\n" \
            "MAIL BODY\n" \
            "MAIL BODY\n"

#attachment file name
send_file_name_as = "attechment_file_name"

#attchment file path
send_file_path = '/attachment/file/path'
'''

#mail server
send_mail_server = 'smtp.mail.com'
send_mail_port = 587

CELERY_BROKER_URL='redis://localhost:6379/0'
