# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 01:31:54 2019

@author: hoped
"""

"""
Part II:
    Now that matches have been generated, time to automate sending some emails 
    with the results containing
    1] Each person's name and their listed interests
    2] Their matches and the interests they share in common
    3] A brief explanation of the algorithm    
"""
import smtplib

from string import Template
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = "" #enter your gmail address
PASSWORD = "" # enter your password. Note you will have to fiddle with some settings

def get_contacts(people):
    """
    @author: byoung
    """
    total = []
    names = []
    email = []
    message = []
    text = "Happy New Year"
    # Get names, emails and msg
    for i in people:
      names.append(i.name)
      email.append(i.email)
      message.append(str(i))
      total.append([names[-1], email[-1], message[-1]])
    return total

def main(people):
    """
    main method for automating emails
    @author: byoung
    """
    total = get_contacts(people)
    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    # For each contact, send the email:
    for name, email, message in total:
        msg = MIMEMultipart() # create a message
        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=email
        msg['Subject']="MAW Dating Algorithm Results"
        message = MIMEText(message)
        # add in the message body
        msg.attach(message)
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()