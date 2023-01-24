import discord

async def command(client, message, config):
    if message.content == "ping on":
        if config["ping_role"] in [role.id for role in message.author.roles]:
            await message.channel.send("you already have the role")
            return
        await message.author.add_roles(discord.utils.get(message.guild.roles, id=config["ping_role"]))
        await message.channel.send("has been added to your roles")

    elif message.content == "ping off":
        if config["ping_role"] in [role.id for role in message.author.roles]:
            await message.author.remove_roles(discord.utils.get(message.guild.roles, id=config["ping_role"]))
            await message.channel.send("has been removed from your roles")
            return
        await message.channel.send("you do not have the role")
