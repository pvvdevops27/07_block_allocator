import gspread_dataframe as gd
from random import randrange
import gspread as gs
from Google import *
import pandas as pd
import datetime
import string
import random


# Block id generator

def block_id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))




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

# Devuelve el sheetId de la petición que contienen un asunto específico si procede

def get_sheet_id(message_subject):
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

            if len(str(messageResource["snippet"]).strip()) > 1:

                return str(messageResource["snippet"]).strip().split(" ")[0]

            else:
                return str(messageResource["snippet"]).strip()

        else:
            return "Not found"

# Selecciona N filas aleatoriamente de un df

def df_random(df, size):
    random_numbers = []
    for number in range(1, len(df)):
        rand_number = randrange(1, size+1)
        if rand_number not in random_numbers:
            random_numbers.append(rand_number)

    random_numbers = random_numbers[0:size+1]

    header = list(df.iloc[0])
    df.iloc[random_numbers].columns = header

    return df.iloc[random_numbers]

# Convierte una hoja de calculo de google sheet a un df

def gsheet_to_df(id, sheet_name):
    gc = gs.service_account(filename='service_account.json')
    sh = gc.open_by_url(
        f'https://docs.google.com/spreadsheets/d/{id}')

    ws = sh.worksheet(f'{sheet_name}')
    df = pd.DataFrame(ws.get_all_records())
    return df


def block_allocator():
    # Conexión con bbdd en google sheets y lectura mediante pandas

    df_bbdd = gsheet_to_df("1C-hTyVGZI1xqQHvRqRsEGDuJoSlSj63h1PzDz3fwSFE", "ddbb")

    # Conexión con pools en google sheets

    df_pools = gsheet_to_df("12B1RyjGdWob34ZZ0jYy6h6mEfuQba1GS7A8Mwxx5pdY", "allocationPool")

    # Asignación del bloque al miembro de Aitana

    # Lectura del id de la hoja de calculo a través de la petición por correo

    sheet_id = get_sheet_id("Block Allocator")

    # Obtiene los parámetros de configuración necesarios para la asignación del bloque

    df_config = gsheet_to_df(sheet_id, "Block configuration")

    size = int(df_config.iloc[0]["blockSize"])
    owner = df_config.iloc[0]["owner"]

    # Seleccion de N rows de forma aleatoria para ser asignadas teniendo en cuenta los cif ya asigandos.

    try:
        cifs_already_allocated = list(df_pools["cif"])
    except: 
        cifs_already_allocated = []
        
    df_bbdd_available = df_bbdd.loc[~df_bbdd['cif'].isin(cifs_already_allocated)]


    allocation_df = df_random(df_bbdd_available, size)


    print(allocation_df)

    # Asignación de columnas que van a aparecer en el bloque

    # Columnas:
    
    current_block_df = pd.DataFrame()
    
    # Company information
    
    cif = allocation_df[["cif"]]
    name = allocation_df[["name"]]
    niche = ""
    charge = allocation_df[["charge"]]
    contactName = allocation_df[["contactName"]]

    # Contact information
    web = allocation_df[["web"]]
    linkedin = allocation_df[["linkedin"]]
    email = allocation_df[["email"]]
    fullAddress = ""
    phone = allocation_df[["phone"]]

    # Connections done
    connectionLinkedinDate = ""
    connectionEmailDate	= ""
    connectionPhoneDate = ""
    connectionAddressDate = ""
    
    # Responses
    responseLinkedinDate = ""
    responseEmailDate = ""
    responsePhoneDate = ""
    responseAddressDate = ""
    
    # Conclusion
    actionType = ""


    # Construccion del dataframe de asignación 

    current_block_df["cif"] = cif
    current_block_df["name"] = name
    current_block_df["niche"] = niche
    current_block_df["charge"] = charge
    current_block_df["contactName"] = contactName
    current_block_df["web"] = web
    current_block_df["linkedin"] = linkedin
    current_block_df["email"] = email
    current_block_df["fullAddress"] = fullAddress
    current_block_df["phone"] = phone


    current_block_df["connectionLinkedinDate"] = connectionLinkedinDate
    current_block_df["connectionEmailDate"] = connectionEmailDate
    current_block_df["connectionPhoneDate"] = connectionPhoneDate
    current_block_df["connectionAddressDate"] = connectionAddressDate
    
    current_block_df["responseLinkedinDate"] = responseLinkedinDate
    current_block_df["responseEmailDate"] = responseEmailDate
    current_block_df["responsePhoneDate"] = responsePhoneDate
    current_block_df["responseAddressDate"] = responseAddressDate

    current_block_df["actionType"] = actionType

    # Escritura en el fichero current correspondiente al miembro de Aitana

    df_to_gsheet(sheet_id, "Block in progress", current_block_df, columns=["cif","name",
            "niche",
            "charge",
            "contactName",
            "web",
            "linkedin",
            "email",
            "fullAddress",
            "phone",
            "connectionLinkedinDate",
            "connectionEmailDate",
            "connectionPhoneDate",
            "connectionAddressDate",
            "responseLinkedinDate",
            "responseEmailDate",
            "responsePhoneDate",
            "responseAddressDate",
            "actionType"])

    # Asignación de columnas que van a aparecer en pools    
    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    blockId = str(block_id_generator())
    pools_df = pd.DataFrame()
    
    pools_df["cif"] = cif

    pools_df["allocatedTo"] = owner
    pools_df["allocationDate"] = now
    pools_df["blockId"] = blockId

    pools_df["name"] = name
    pools_df["niche"] = niche
    pools_df["contactName"] = contactName
    pools_df["charge"] = charge
    pools_df["linkedin"] = linkedin
    pools_df["email"] = email
    pools_df["phone"] = phone
    pools_df["web"] = web
    pools_df["fullAddress"] = fullAddress

    # Escritura en pools

    df_to_gsheet("12B1RyjGdWob34ZZ0jYy6h6mEfuQba1GS7A8Mwxx5pdY", "allocationPool", pools_df, columns=["allocatedTo","allocationDate",
            "blockId",
            "cif",
            "name",
            "niche",
            "contactName",
            "charge",
            "linkedin",
            "email",
            "phone",
            "web",
            "fullAddress"
            ])

    
    # Borrado de la petición y registro de actividad en los logs del contenedor

block_allocator()
