#!/usr/bin/env python
# -*- coding: utf8 -*-

import ntpath
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email:
    def __init__(self, server_username, server_password, server_address="smtp.gmail.com", server_port=587):
        self.server_address = server_address
        self.server_port = server_port
        self.server_username = server_username
        self.server_password = server_password

    def send_email(self, from_address, to_address, subject, body):
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP(self.server_address, self.server_port)
        server.starttls()
        server.login(from_address, self.server_password)
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()

    def send_email_with_attachments(self, from_address, to_address, subject, body, file_paths):
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        for file_path in file_paths:
            filename = ntpath.basename(file_path)
            attachment = open(file_path, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            msg.attach(part)
        server = smtplib.SMTP(self.server_address, self.server_port)
        server.starttls()
        server.login(from_address, self.server_password)
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
