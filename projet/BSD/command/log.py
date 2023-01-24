import mod.conf as conf
import os

async def log_bot(channel):
    msg = "**LOG**"
    for f in os.listdir(f"{conf.path}bot/log"):
        with open(f"{conf.path}bot/log/{f}", "r") as file:
            cont = file.read()
        if cont != "":
            msg += f"\n{f}:\n```\n{cont}\n```"
    await channel.send(f"{msg[:1950]}```...")
