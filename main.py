import requests
import classeviva
import time
from time import strftime
import asyncio
from discord_webhook import *

with open("config.txt", "a+") as f:
    f.seek(0)
    credentials = f.readline()
    webhook_URL = f.readline()
    try:
        username = credentials.split(" ")[0]
        password = credentials.split(" ")[1].replace("\n", "")
        webhook_URL[0] # If it works don't touch it
    except:
        username = input("Please enter your username : ")
        password = input("Please enter your password : ")
        webhook_URL = input("Please paste your discord webhook URL : ")

        save_config = "";
        while save_config.lower() != "y" and save_config.lower() != "n":
            save_config = input("Would you like to save your configuration to use it automatically? (y/n) : ")
            if save_config.lower() == 'y':
                f.write(f"{username} {password}\n{webhook_URL}")

utente = classeviva.Utente(username, password)

def updateBacheca():
    utente()

    bacheca = asyncio.run(utente.bacheca())

    bacheca.reverse()

    for comunicazione in bacheca:
        with open("comunicazioni.txt", "a+") as f:
            f.seek(0)
            if f.read().__contains__(str(comunicazione["pubId"])):
                continue

            webhook = DiscordWebhook(webhook_URL)

            embed = DiscordEmbed(comunicazione["cntTitle"].replace("0 - ", ""))
            embed.set_color(0xff0000)
            embed.set_footer(text=comunicazione["cntValidFrom"], icon_url="https://www.secondocomprensivo.edu.it/wp-content/uploads/2022/08/ClasseViva.jpg")
            webhook.content = "||<@&1434286238470504458>||"

            webhook.add_embed(embed)
            webhook.allowed_mentions = {"roles" : ["1434286238470504458"]}

            webhook.execute()

            f.write(f"{comunicazione["pubId"]}\n")

            time.sleep(5)

while True:
    if int(strftime("%M")) % 10 == 7:
        updateBacheca()
    time.sleep(10)