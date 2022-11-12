import datetime
import discord
import bot

intents = discord.Intents.all()
client = discord.Client(intents=intents)

bird = 229401751281729536
alex = 298206761587048448
prefix = '.'


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
    print(msg)
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


    if msg.startswith(".hello"):
        await channel.send("Hello!")

    elif msg.startswith(f'{prefix}l'):
        if is_pChat:
            await channel.send(bot.take_L(user))

    elif msg.startswith(f'{prefix}stats') or msg.startswith(f'{prefix}profile'):
        if mentions:
            await channel.send(embed=bot.stats(mentioned))
        else:
            await channel.send(embed=bot.stats(user))

    elif msg.startswith(f'{prefix}setpchat'):
        await channel.send(bot.set_pChat(channel, server))

    elif msg.startswith(f'{prefix}setcchat'):
        await channel.send(bot.set_cChat(channel, server))

    elif msg.startswith(f'{prefix}setqchat'):
        await channel.send(bot.set_qChat(channel, server))

    elif msg.startswith(f'{prefix}pushup'):
        await channel.send(bot.pushup(user))

    elif msg.startswith(f'{prefix}addsum'):
        print('loladd')
        await channel.send(bot.add_summoner(user,message.content[7:]))


    if is_cChat:
        bot.counted(user)

    if is_qChat:
        if mentions:
            bot.quote(message.content, mentioned)

    if user.id == bird:
        if not is_cChat:
            if not is_qChat:
                # await message.reply(content="SYM Bird")
                await message.add_reaction('🐔')


    elif user.id == alex:
        if msg.startswith(f'{prefix}qreload'):
            if is_qChat:
                print("Reloading Quotes...")
                bot.users.update({'quote': []})
                async for x in channel.history(oldest_first=True, limit=9999):
                    m = x.mentions
                    if m:
                        for y in m:
                            bot.quote(x.content, y)

        elif msg.startswith(f'{prefix}creload'):
            if is_cChat:
                print("counting Counters...")
                async for x in channel.history(oldest_first=True, limit=9999, after=datetime.datetime(2022, 10, 22)):
                    bot.counted(x.author)

        elif msg.startswith(f'{prefix}allstop'):
            exit()



client.run(bot.TOKEN)
