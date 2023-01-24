'''    _             _
  ___ | | _   _   __| | _ __   ___
 / _ \| || | | | / _` || '__| / _ |
|  __/| || |_| || (_| || |   |  __/
 \___||_| \__, | \__,_||_|    \___|
          |___/
___________________________________

 - codé en : UTF-8
 - langage : python3
 - GitHub  : github.com/elydre
 - Licence : GNU GPL v3
'''

#import
import discord, sys

# bot
client = discord.Client()


@client.event
async def on_ready():
    ch = client.get_channel(880053539110522910)
    messages = await ch.history(limit=1).flatten()
    for each_message in messages:
        drmsg = each_message.content
    temp = "".join(f'{guild.name}: {str(guild.member_count)} membres' + "\n" for guild in client.guilds)

    temp = temp.split("\n")

    # saute de ligne automatique
    drmsgn = drmsg
    drmsg = list(drmsg)
    if len(drmsg) > 20:
        drmsgn = ""
        for x in range(len(drmsg)):
            drmsgn += "." if x > 56 else drmsg[x]
            if x in [20, 39] and len(drmsg) not in [21, 40]:
                drmsgn += "\n| "



    msg = temp[0] +  "\nnvifgudhihgifukdh" + drmsgn
    with open("/home/pi/nas-kit-master/data.txt", "w") as fil:
        fil.write(str(msg))
    sys.exit()


client.run("token")