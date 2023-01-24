import sys, os, json
from time import sleep

import discord
import mod.conf as conf
from command.log import log_bot
from command.start import start_bot
from command.stop import stop_bot

bot = discord.Client()

on_bots = []

bot_paths = json.load(open(f"{conf.path}mod/path.json"))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    await bot.get_channel(conf.log_channel).send("Ready!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name= conf.bot_info))
    for cible in bot_paths.keys():
        if cible not in on_bots:
            on_bots.append(cible)
            await start_bot(cible, 0, bot, bot_paths)
            sleep(1)


@bot.event
async def on_message(message):
    global bot_paths
    if (message.author.id not in conf.admins) or (message.channel.id not in conf.ctrl_channels):
        return

    if message.content.startswith("ping"):
        await message.channel.send("pong")

    elif message.content.startswith("boot"):
        for cible in conf.bots.keys():
            on_bots.append(cible)
            await start_bot(cible, message.channel, bot, bot_paths)
            sleep(1)

    elif message.content.startswith("crash"):
        sys.exit(0)

    elif message.content.startswith("run"):
        await message.channel.send(", ".join(on_bots))

    elif message.content.startswith("go"):
        if len(message.content.split(" ")) == 1:
            await message.channel.send("Please specify a bot name")
        else:
            cible = message.content.split(" ")[1]
            on_bots.append(cible)
            await start_bot(cible, message.channel, bot, bot_paths)

    elif message.content.startswith("stop"):
        if len(message.content.split(" ")) == 1:
            await message.channel.send("Please specify a bot name")
        else:
            cible = message.content.split(" ")[1]
            on_bots.remove(cible)
            await stop_bot(cible, message.channel, bot, bot_paths)

    elif message.content.startswith("list"):
        await message.channel.send("```\n" + "\n".join([f"{name}: {bot_paths[name]}" for name in bot_paths.keys()]) + "\n```")

    elif message.content.startswith("help"):
        await message.channel.send(conf.discord_help)

    elif message.content.startswith("rld"):
        await message.channel.send("Reloading json file...")
        bot_paths = json.load(open(f"{conf.path}mod/path.json"))
        await message.channel.send("Done!")

    elif message.content.startswith("log"):
        await log_bot(message.channel)

bot.run(conf.token)
