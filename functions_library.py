from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import gspread_dataframe as gd
from random import randrange
import gspread as gs
from Google import *
import pandas as pd
import datetime
import string
import base64
import random
import json


def get_email_id(message_subject):
    CLIENT_SECRET_FILE = './client_secret.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(
        CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(
        userId='me', labelIds=['INBOX'], maxResults=5).execute()

    messages = results.get('messages', [])

    for message in messages:
        messageResource = service.users().messages().get(
            userId="me", id=message['id']).execute()
        headers = messageResource["payload"]["headers"]

        subject = [j['value']
                   for j in headers if j["name"] == "Subject"]

        if subject[0] == message_subject:
            return message["id"]

# # Elimina un mensaje de gmail


def delete_message(message_id):
    CLIENT_SECRET_FILE = "./client_secret.json"
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    service.users().messages().delete(userId='me', id=message_id).execute()
    return 'Message with id: %s deleted' % message_id

# # Elimina la petición realizada


def delete_request(message_subject):
    try:
        delete_message(get_email_id(message_subject))
        return "success"
    except:
        return "No requests founded"


# Convierte un df a una hoja de calculo de google sheet
def df_to_gsheet(sheet_id, sheet_name, df, columns):
    try:

        gc = gs.service_account(filename='service_account.json')
        sh = gc.open_by_url(
            f'https://docs.google.com/spreadsheets/d/{sheet_id}')

        ws = sh.worksheet(f'{sheet_name}')
        existing_df = gd.get_as_dataframe(ws)[columns].dropna(how='all')

        data = [existing_df, df]
        updated_df = pd.concat(data, axis=0)

        gd.set_with_dataframe(ws, updated_df)

        return "Success"

    except:
        return "Error"


# Registra la actividad realizada por Aitana
def logger(tool):
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    with open('logs.txt', 'a') as the_file:
        the_file.write(f'{timestamp} | {tool} was activated\n')

# Escribe los resultados en output


def output_gsheet_writer(id, df_output):
    df_to_gsheet(id, "Output", df_output, columns=["email", "status"])

# Ecribe los resultados en output en los logs


def logs_gsheet_writer(id, df_output):
    df_to_gsheet(id, "Logs", df_output, columns=["email", "dateSent"])

# Google sheet a dataframe


def gsheet_to_df(id, sheet_name):
    gc = gs.service_account(filename='service_account.json')
    sh = gc.open_by_url(
        f'https://docs.google.com/spreadsheets/d/{id}')

    ws = sh.worksheet(f'{sheet_name}')
    df = pd.DataFrame(ws.get_all_records())
    return df

# Función de envio de email


def gmail_sender(subject, message, to):

    CLIENT_SECRET_FILE = './src/client_secret.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    emailMsg = message
    mimeMessage = MIMEMultipart()
    mimeMessage['from'] = 'Pablo Viteri <pablo.viteri@twigspain.com>'
    mimeMessage['to'] = to
    mimeMessage['subject'] = subject
    mimeMessage.attach(MIMEText(emailMsg, 'html'))

    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
    message = service.users().messages().send(
        userId='me', body={'raw': raw_string}).execute()

    print(message)
