import discord
import mod.cmds as cmds
import mod.tools as tools
import mod.usr as usr
import json

config = json.load(open("config.json"))

intents = discord.Intents.all()
client = discord.Client(intents=intents)

global command_to_confirm
command_to_confirm = None

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")

@client.event
async def on_message(message):
    global command_to_confirm

    if message.author == client.user:
        return

    if message.content == "info":
        if await tools.have_not_perm(config, message): return
        await tools.send_info(message)


    if message.channel.id == config["chan"]["cmd"]:
        if await tools.have_not_perm(config, message): return
        command_to_confirm = await cmds.command(client, message, config, command_to_confirm)

    if message.channel.id == config["chan"]["usr"]:
        await usr.command(client, message, config)


client.run(config["token"])
