async def have_not_perm(config, message):
    if config["cmd_role"] in [role.id for role in message.author.roles]:
        return False
    await message.channel.send("you do not have the required role to use this command")
    return True

async def send_info(message):
    msg = "```\n"
    msg += f"channel id: {message.channel.id}\n"
    msg += f"author id: {message.author.id}\n"
    msg += f"author name: {message.author.name}\n"
    msg += f"author discriminator: {message.author.discriminator}\n"
    msg += f"author roles: {message.author.roles}\n```"

    await message.channel.send(msg)