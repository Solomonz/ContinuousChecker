#! /usr/bin/env python3

from json import load
from smtplib import SMTP_SSL
from sys import exit
from time import sleep
from twilio.rest import Client


def format_message(text, label='', index=0, total=1):
    if index < 0 or total < 1 or index >= total:
        raise Exception('malformed input to format_message')

    if index == 0 and total == 1:
        return '.{}\n\n{}'.format('\n\n{}'.format(label) if len(label) > 0 else '', text)

    def spaced_label_and_counter():
        prefix = '\n\n{}'.format(label)
        if len(label) > 0:                          
            prefix = '{}  '.format(prefix)
        return '{}({}/{})'.format(prefix, index + 1, total)

    return '.{}\n\n{}'.format(spaced_label_and_counter(), text)


def send_text(client, from_, to, text, label=''):
    portion_size = 1530 - len(label)
    submessages = [text[i:i+portion_size] for i in range(0, len(text), portion_size)]
    for i, m in enumerate(submessages):
        if i > 0:
            sleep(5)
        client.messages.create(to=to, from_=from_, body=format_message(text=m, label=label, index=i, total=len(submessages)))


def notify(item, location, url=None):
    with open('credentials.json') as creds_file:
        creds = load(creds_file)
        twilio_creds = creds['twilio']
        account_sid = twilio_creds['account_sid']
        auth_token = twilio_creds['auth_token']
        account_number = twilio_creds['account_number']

        email_creds = creds['email']
        email_server_address = email_creds['address']
        email_server_password = email_creds['password']
    
    with open('watcher_info.json') as watcher_file:
        watcher_info = load(watcher_file)
        watcher_email = watcher_info['email']
        watcher_number = watcher_info['phone_number']
    
    twilio_client = Client(account_sid, auth_token)
    text = "{item} is available from {location}{extra_info}".format(item=item, location=location, extra_info="\n\nSupplied url:   {url}".format(url=url) if url is not None else "")

    send_text(twilio_client, account_number, watcher_number, text)

    try:
        server = SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(email_server_address, email_server_password)
        body = "Go get em!"
        if url is not None:
            body = "Supplied url is {url}".format(url=url)
        server.sendmail(email_server_address, watcher_email, 'From: {server_addr}\nTo: {user_addr}\nSubject: [Mail Server] {item} is available from {location}\n{body}'.format(server_addr=email_server_address, user_addr=watcher_email, item=item, location=location, body=body))
        server.close()
    except Exception as e:
        print('Something went wrong with sending an email!\nYou may need to enable access to less secure apps at {}'.format('https://myaccount.google.com/lesssecureapps'))
        print(e)
        exit(1)
