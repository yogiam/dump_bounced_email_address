# Small program to extract the destination email id which bounced.
# Code borrowed from the link below and updated to fit my requirement.
# https://www.thepythoncode.com/article/reading-emails-in-python

import imaplib
import email
from email.header import decode_header

# account credentials
username = "user@exmaple.com"
password = "mystrongpassword"

# create an IMAP4 class with SSL 
imap = imaplib.IMAP4_SSL("imap.asia.myemailprovider.com")
# authenticate
imap.login(username, password)
# print('login done..')

status, messages = imap.select("INBOX")

# total number of emails
messages = int(messages[0])

for i in range(messages + 1):
    # fetch the email message by ID
    res, msg = imap.fetch(str(i), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            # parse a bytes email into a message object
            msg = email.message_from_bytes(response[1])
            # decode the email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                # if it's a bytes, decode to str
                subject = subject.decode(encoding)
            # decode email sender
            From, encoding = decode_header(msg.get("From"))[0]
            if isinstance(From, bytes):
                From = From.decode(encoding)
            # print("\n\nSubject:", subject)
            # print("From:", From)
            # if the email message is multipart
            if msg.is_multipart():
                # iterate over email parts
                for part in msg.walk():
                    # extract content type of email
                    content_type = part.get_content_type()
                    # print(content_type)
                    if content_type == "message/delivery-status":
                        try:
                            # get the body from the part
                            lines = part.get_payload()
                            # body is a list of strings, extract the one with 'Final-recipient' in it and split
                            lines = [str(line).strip().lower() for line in lines]
                            lines = [line for line in lines if "final-recipient" in line]
                            # sometimes there is more content after the email id separated by a \n.
                            # split and take only the first line.
                            lines = [line for line in lines[0].split("\n")]
                            print(str(lines[0].split(";")[1]).strip())
                        except Exception as e:
                            # I haven't tested all the possibilities, exceptions need to be handled.
                            pass
# close the connection and logout
imap.close()
imap.logout()
