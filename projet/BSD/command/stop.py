import mod.conf as conf
import os

async def stop_bot(name, channel, bot):
    with open(f"{conf.path}bot/pid/{name}.pid", "r") as f:
        pid = f.read().replace("\n", "").strip()
    if pid:
        os.system(f"kill {pid}")
        print(f"{name} stopped with pid {pid}")
        await bot.get_channel(conf.log_channel).send(f"**{name}** stopped (pid: {pid})")
        await channel.send(f"**{name}** stopped (pid: {pid})")
    else:
        print(f"{name} not found")
        await channel.send(f"**{name}** not found")