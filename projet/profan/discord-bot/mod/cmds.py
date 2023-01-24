import requests, discord

async def release(r, channel, ping_id = 0):
    message = "type **go** for post" if ping_id == 0 else f"<@&{ping_id}> come see, there is something new!"
    dico = {
        "title": r["name"],
        "url": f"https://elydre.github.io/profan/release?{r['release']}",
        "description": f"profanOS **{r['release']}** joins main updates!",
        "color": 0x53927c,
        "image": {
            "url": f"https://elydre.github.io/img/profan/{r['name'].split(' ')[1]}.png"
        }
    }
    await channel.send(message, embed=discord.Embed.from_dict(dico))

async def latest(r, channel, ping_id = 0):
    message = "type **go** for post" if ping_id == 0 else f"<@&{ping_id}> come see, there is something new!"
    nom = r["name"].replace("-", " ")[:-4]
    dico = {
        "title": nom,
        "url": f"https://elydre.github.io/profan/release?{nom.split(' ')[1]}",
        "description": f"{nom} was released!",
        "color": 0xbb1341,
    }
    await channel.send(message, embed=discord.Embed.from_dict(dico))

async def command(client, message, config, ctc):
    if message.content == "rs":
        api = requests.get(config["url"]["release"])
        if api.status_code != 200:
            await message.channel.send("error getting release info")
            return
        r = api.json()[-1]
        await release(r, message.channel)
        return lambda: release(r, client.get_channel(config["chan"]["release"]), config["ping_role"])

    if message.content == "lt":
        api = requests.get(config["url"]["latest"])
        if api.status_code != 200:
            await message.channel.send("error getting latest info")
            return
        r = api.json()[-1]
        await latest(r, message.channel)
        return lambda: latest(r, client.get_channel(config["chan"]["latest"]), config["ping_role"])

    if message.content == "go":
        if ctc is None:
            await message.channel.send("no command to confirm")
            return
        await ctc()
        return None
