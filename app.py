from flask import Flask, jsonify
from flask import request
import redis
from email import MIMEMultipart
from email import MIMEText
from email import MIMEBase
from email import encoders
from celery import Celery
from celery.utils.log import get_logger
from settings import *
from task import *


app = Flask(__name__)
logger = get_logger(__name__)




'''
get setting from settings.py
'''
#app.config.from_object(settings)

#redisobj = redis.StrictRedis(host='localhost', port=6379, db=0)
celery = Celery(app.import_name, broker=CELERY_BROKER_URL)
celery.conf.update(app.config)



@app.route('/mail', methods=['POST'])
def send_mail():
    
    '''
    {
	"to_address_dict": {
		"To": [
			"karan.bhalodiya@einfochips.com"
		],
		"CC": [
			"karan.bhalodiya@einfochips.com"
		],
		"BCC": [
			"karan.bhalodiya@einfochips.com"
		]
	},
	
    "subject" : "Test mail from python script",
	
	"mail_body" : "MAIL BODY\n" 
    }
    '''

    #check if param is provided & properly or not
    if not request.json or not 'to_address_dict' in request.json:
    	return jsonify({"error":"param 'Email Address' not found in json or json has not been prepared properly"}), 400  

    addr_dict = request.json["to_address_dict"]
    subject = request.json["subject"]
    mail_body = request.json["mail_body"]

    task = sendMail.apply_async(args=[SMTP_USER_NAME, addr_dict, subject, mail_body, send_mail_server, SMTP_PASSWORD, send_mail_port])
    '''
    if result.state == "SUCCESS":
    	print "Mail send successfully"
    elif result.state == "FAILURE":
    	print "Failed to send mail"
    else:
		print "Failed sending mail"
    '''
    
    return jsonify({'taksid':str(task)}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
