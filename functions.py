from random import randrange
import pandas as pd
import gspread as gs


# Lectura del sheetId





# Selecciona N filas aleatoriamente de un df

def df_random(df, size):
    random_numbers = []
    for number in range(1, len(df)):
        rand_number = randrange(1, size+1)
        if rand_number not in random_numbers:
            random_numbers.append(rand_number)

    random_numbers = random_numbers[0:size+1]

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

    # Ordenar de mayor a menor facturación

    df_bbdd_sorted = df_bbdd.sort_values(
        "revenue", ascending=False)

    # Conexión con pools en google sheets

    df_pools = gsheet_to_df("12B1RyjGdWob34ZZ0jYy6h6mEfuQba1GS7A8Mwxx5pdY", "allocationPool")

    # Asignación del bloque al miembro de Aitana

    # Lectura del id de la hoja de calculo a través de la petición por correo

    # Seleccion de N rows de forma aleatoria para ser asignadas

    df_random(df_bbdd, 50)

    # Escritura en el fichero current correspondiente al miembro

    # Registro en pools

    






print(block_allocator())



