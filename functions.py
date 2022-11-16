from functions_library import *
import datetime

# Envio de email masivos de un dataframe


def massive_email_sender(id, sheet_name):

    df = gsheet_to_df(id, sheet_name)

    print(df)
    # Massive email send

    config_df = gsheet_to_df(id, "Config")

    message = list(config_df["message"])[0]

    subject = list(config_df["subject"])[0]

    cc = list(config_df["cc"])[0]
    timestamp = []
    for index, row in df.iterrows():
        email = row["email"]+","+cc

        signature = '<br>--<br><div dir="ltr"><b><span style="font-size:12.0pt;color:#002451" lang="ES"></span></b><img src="https://ci3.googleusercontent.com/mail-sig/AIorK4xfn53eCYBGGyGiEE0qw8RXKkwJq1lb0Jb78GWtswbSEMSrJX1RTi3umf-9PFJeLdvtjn0Z4Ho" alt="logo_twig"><br><p class="MsoNormal"><b><span style="font-size:12.0pt;color:#002451" lang="ES">Pablo Viteri</span></b></p><p class="MsoNormal"><b><span style="font-size:12.0pt;color:#002451" lang="ES">Director general</span></b><span style="font-size:12.0pt;color:black" lang="ES"></span></p><p class="MsoNormal"><span style="color:#002451" lang="ES"><u></u>&nbsp;<u></u></span></p><p class="MsoNormal"><span style="font-size:12.0pt;color:#002451" lang="ES">&nbsp;<b>D</b>: Paseo de la Castellana 91, 4 planta</span><span lang="ES"><u></u><u></u></span></p><p class="MsoNormal"><span style="font-size:12.0pt;color:#002451" lang="ES">&nbsp;<b>T</b>: +34 911 847 830</span><span lang="ES"></span></p><p class="MsoNormal"></p><p class="MsoNormal"><span style="font-size:12.0pt;color:#002451" lang="ES">&nbsp;<b>E</b>: <a href="mailto:pablo.viteri@twigspain.com" target="_blank"><span style="color:#0563c1">pablo.viteri@twigspain.com</span></a></span><span style="font-size:11.5pt;color:#201f1e" lang="ES"><u></u><u></u></span></p><p class="MsoNormal"><span style="font-size:12.0pt;color:#002451" lang="ES">&nbsp;<b>W</b>:&nbsp;<a href="http://twigspain.com" target="_blank">twigspain.com</a></span><span style="font-size:12.0pt;color:black" lang="ES"><u></u><u></u></span></p><span style="font-size:12.0pt;color:#002451" lang="ES">&nbsp;<b>L</b>: &nbsp;<a href="https://www.linkedin.com/in/pablo-v-39901a1a3/" target="_blank"><span style="color:#0563c1">LinkedIn</span></a></span></div>'
        gmail_sender(subject, message+signature, email)
        timestamp.append(
            datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))

    # Writing output
    df_output = pd.DataFrame(columns=["email", "status"])
    df_output["email"] = list(df["email"])
    df_output["status"] = "success"

    output_gsheet_writer(id, df_output)

    # Writing logs drive
    df_logs = pd.DataFrame(columns=["email", "dateSent"])
    df_logs["email"] = list(df["email"])
    df_logs["dateSent"] = timestamp

    logs_gsheet_writer(id, df_logs)

    # Internal log

    logger("Massive Email Sender")


    