import datetime
import time

import discord
import bot


intents = discord.Intents.all()
client = discord.Client(intents=intents)

bird = 229401751281729536
alex = 298206761587048448
prefix = '.'
hearth_p = 832504799533596673

pushup_channel = client.get_channel(hearth_p)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    guilds = client.guilds
    lol_reload.start()

    for x in guilds:
        bot.is_server(x)


@client.event
async def on_message(message):
    user = message.author
    if user == client.user:
        return
    # bot.is_user(user)
    msg = str.lower(message.content)
    # print(msg)
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

    elif msg.endswith(f'{prefix}l'):
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

    elif msg.startswith(f'{prefix}link lol'):
        #print('loladd')
        await channel.send(bot.add_summoner(user, message.content[9:]))

    elif msg.startswith(f'{prefix}lol stats'):
        if mentions:
            try:
                await channel.send(embed=bot.lol_stats(mentioned))
            except:
                await channel.send(bot.lol_stats(mentioned))
        else:
            try:
                await channel.send(embed=bot.lol_stats(user))
            except:
                await channel.send(bot.lol_stats(user))

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

        elif msg.startswith(f'{prefix}update 20'):
            bot.update_20()


@discord.ext.tasks.loop(minutes=2.5, reconnect=True)
async def lol_reload():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"{current_time}> Searching for Games...")
    reload = await bot.lol_reload()
    if reload:
        pushup_channel.send(reload)


client.run(bot.TOKEN)

