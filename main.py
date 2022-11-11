import datetime
import discord
import bot

intents = discord.Intents.all()
client = discord.Client(intents=intents)

bird = 229401751281729536


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    guilds = client.guilds

    for x in guilds:
        bot.is_server(x)


@client.event
async def on_message(message):
    user = message.author
    if user == client.user:
        return
    # bot.is_user(user)
    msg = str.lower(message.content)
    channel = message.channel
    server = message.guild
    mentions = message.mentions
    mentioned = None
    for x in mentions:
        bot.is_user(x)
        mentioned = x

    is_pChat = bot.is_pChat(channel)
    is_cChat = bot.is_cChat(channel)
    is_qChat = bot.is_qChat(channel)
    """
    print(f"is_pChat = {is_pChat}")
    print(f"is_cChat = {is_cChat}")
    print(f"is_qChat = {is_qChat}")
    print(f"Message: {msg} Sent By: {message.author}")
    """

    if msg.startswith(".hello"):
        await channel.send("Hello!")

    elif msg.startswith('.l'):
        if is_pChat:
            await channel.send(bot.take_L(user))

    elif msg.startswith('.stats'):
        if mentions:
            await channel.send(bot.stats(mentioned))
        else:
            await channel.send(bot.stats(user))

    elif msg.startswith('.setpchat'):
        await channel.send(bot.set_pChat(channel, server))

    elif msg.startswith('.setcchat'):
        await channel.send(bot.set_cChat(channel, server))

    elif msg.startswith('.setqchat'):
        await channel.send(bot.set_qChat(channel, server))

    elif msg.startswith('.qreload'):
        if is_qChat:
            print("Reloading Quotes...")
            async for x in channel.history(oldest_first=True, limit=9999):
                print(x.content)
                m = x.mentions
                if m:
                    for y in m:
                        bot.quote(x.content, y)

    elif msg.startswith('.creload'):
        if is_cChat:
            print("counting Counters...")
            async for x in channel.history(oldest_first=True, limit=9999, after=datetime.datetime(2022, 10, 22)):
                bot.counted(x.author)

    if is_cChat:
        bot.counted(user)

    if is_qChat:
        if mentions:
            bot.quote(msg, mentioned)

    if user.id == bird:
        if not is_cChat:
            if not is_qChat:
                await message.reply(content="SYM Bird")
                await message.add_reaction('😑')



client.run('MTA0MDEyNTQ0MTQyOTczMzM3Ng.GIabJt.yMARvCgxhez8XZFtxtDsIDhQpit1rVe1l5XL3Q')
