import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    # TODO: Get connection to database
    connection = psycopg2.connect(
                                database=os.getenv("POSTGRES_DB"), 
                                user=os.getenv("POSTGRES_USER"), 
                                password=os.getenv("POSTGRES_PW"), 
                                host=os.getenv("POSTGRES_HOST"), 
                                port=5432)

    cursor = connection.cursor()                            

    try:
        # TODO: Get notification message and subject from database using the notification_id
        cursor.execute( '''SELECT message, subject
                          FROM notification
                          WHERE id = {}
                        '''.format(notification_id))
        
        notification = cursor.fetchone()

        # TODO: Get attendees email and name
        cursor.execute('''SELECT email, first_name
                          FROM attendee
                       ''')
        
        attendees = cursor.fetchall()

        # TODO: Loop through each attendee and send an email with a personalized subject
        for attendee in attendees:
            email = attendee[0]
            first_name = attendee[1]
            
            subject = '{}: {}'.format(first_name, notification[1])
            send_email(email, subject, notification[0])

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        status = 'Notified {} attendees'.format(len(attendees))
        cursor.execute('''UPDATE notification 
                          SET status = '{}', completed_date = '{}' 
                          WHERE id = {};
                       '''.format(status, datetime.utcnow(), notification_id))
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        # TODO: Close connection
        if connection:
            cursor.close()
            connection.close()

def send_email(recipients, subject, body):
    smtp_server = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_sender = os.getenv("SMTP_SENDER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    msg = MIMEMultipart()
    msg['From'] = smtp_sender
    msg['To'] = recipients
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Connect to SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls() 
        
        # Log in server
        server.login(smtp_sender, smtp_password)
        
        # Send the email
        server.sendmail(smtp_sender, recipients, msg.as_string())
        
        # Disconnect server
        server.quit()
        
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Email sent failure. Error: {e}")
