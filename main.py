from asyncio.windows_events import NULL
import discord
from discord import channel
from discord.message import MessageType
import os.path
from email_sender import EmailSender
import re


emails = list()
client = discord.Client()


def write_emails(mails):
    for mail in mails:
        with open('emails.txt','a') as f:
            f.write(mail+"\n")

def send_email(): 
    gmail_user = 'YourEmail@gmail.com'
    gmail_pwd = 'PasswordToYourEmail'

    try:
        es = EmailSender('smtp.gmail.com',465)
        es.login(gmail_user, gmail_pwd)
        for email in emails:
            es.send("Text of email","Title of email",email)
            print("Successfully sent the mail to "+email)
            emails.remove(email)
    except: print("failed to send mail to "+email)

def refresh_file(file):
    file.close()
    open(file, "a")

@client.event
async def on_ready():
    print('Logged in as:'+client.user.name)


@client.event
async def on_message(message):
    if message.content == "!list":
        for email in emails:
            await client.send_message(message.channel, content=str(email))

    elif message.content[:4] == "!add":
        email = message.content[5:]
        print("Trying to add "+message.content[5:]+" to emails")
        if email not in emails:
            emails.append(message.content[5:])
            print("Added "+message.content[5:]+" to emails")
            write_emails(emails)

        else:
            print("Email is already in emails")

    elif message.content[:4] == "!del":
        print("Removed "+message.content[5:]+" from emails")
        write_emails(emails, message.content[5:])
        

    while True:
        for email in emails:
            send_email()
            print(f"Email sended to {email}")
                


client.run('YourToken')
