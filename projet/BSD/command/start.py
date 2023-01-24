import mod.conf as conf
import os

async def start_bot(name, channel, bot, bot_paths):
    if name in bot_paths.keys():
        cmd = f"{bot_paths[name]} > {conf.path}bot/log/{name}.log 2>&1 & echo $! > {conf.path}bot/pid/{name}.pid"
        os.system(cmd)
        print(f"{name} started")
        await bot.get_channel(conf.log_channel).send(f"**{name}** started")
        if channel: await channel.send(f"**{name}** started")
    else:
        print(f"{name} not found")
        if channel: await channel.send(f"**{name}** not found")
