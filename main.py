import datetime
import time
from random import choice
import random
import discord
from discord.ext import commands
import bot

intents = discord.Intents.all()
client = commands.Bot(intents=intents)

game_answer = None
hearth = 695056946616860729
bird = 229401751281729536
alex = 298206761587048448
prefix = 'i am incredibly homosexual'
hearth_p = 832504799533596673
pg = False
sorts = ["l_wins",
         "l_losses",
         "l_kills",
         "l_deaths",
         "l_max_kill",
         "l_assists",
         "l_pentas",
         "l_quadras",
         "l_games",
         "l_win_streak",
         "l_loss_streak"
         ]

birds = ["🦃", "🐔", "🐓", "🐣", "🐤", "🐥", "🐦", "🦆", "🐧"]
idx = 1

help = discord.Embed(title="***🤖Bot Commands🤖***",
                     description="All commands are in ***l o w e r - c a s e***")
help.add_field(name="Take L", value='/l', inline=False)
help.add_field(name="Do Pushups", value='/pushup', inline=False)
help.add_field(name="View Hearth Stats", value='/stats [optional @User]', inline=False)
help.add_field(name="Link League Account", value='/link-lol [summoner name]', inline=False)
help.add_field(name="View League Stats", value='/lol-stats [optional @User]', inline=False)
help.add_field(name="View League Leaderboard", value='/lol-top', inline=False)
help.add_field(name="Get a Random Quote", value='/random-quote', inline=False)
help.add_field(name="Guess who said the Quote", value='/answer', inline=False)
help.add_field(name="Get Bot Commands", value='/help', inline=False)


# help2.set_footer(text="Page 2")


@client.event
async def on_ready():
    global gID
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
    msg = str.lower(message.content)
    channel = message.channel
    server = message.guild
    mentions = message.mentions
    mentioned = None
    for x in mentions:
        bot.is_user(x)
        mentioned = x

    is_cChat = bot.is_cChat(channel)
    is_qChat = bot.is_qChat(channel)

    if msg.startswith(f'{prefix}setpchat'):
        await channel.send(bot.set_pChat(channel, server))

    elif msg.startswith(f'{prefix}setcchat'):
        await channel.send(bot.set_cChat(channel, server))

    elif msg.startswith(f'{prefix}setqchat'):
        await channel.send(bot.set_qChat(channel, server))

    if is_cChat:
        bot.counted(user)

    if is_qChat:
        if mentions:
            bot.quote(message.content, mentioned)

    if user.id == bird:
        if not is_cChat:
            if not is_qChat:
                if random.randint(0, 4) == 1:
                    sym = random.randint(0, 9)
                    if sym == 1:
                        await message.add_reaction('🇸')
                        await message.add_reaction('🇾')
                        await message.add_reaction('🇲')
                        await message.add_reaction('🇧')
                        await message.add_reaction('🇮')
                        await message.add_reaction('🇷')
                        await message.add_reaction('🇩')
                    else:
                        await message.add_reaction(choice(birds))


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


ment = discord.Option(discord.User, description="@User", reqired=False, default='')


@client.slash_command(name="stats", guild_ids=[hearth],
                      description='View Hearth Stats')
async def stats(ctx, mention: ment):
    user = mention
    if not mention:
        user = ctx.user
    await ctx.respond(embed=bot.stats(user))


@client.slash_command(name="l", guild_ids=[hearth],
                      description='Take an L')
async def l(ctx):
    if bot.is_pChat(ctx.channel):
        await ctx.respond(bot.take_L(ctx.user))
    else:
        await ctx.respond("This isn't the channel for that!")


@client.slash_command(name="lol-stats", guild_ids=[hearth],
                      description='View League Stats')
async def lol_stats(ctx, mention: ment):
    user = mention
    if not mention:
        user = ctx.user
    try:
        await ctx.respond(embed=bot.lol_stats(user))
    except:
        await ctx.respond(bot.lol_stats(user))


@client.slash_command(name="help", guild_ids=[hearth],
                      description="View Bot Commands")
async def hlp(ctx):
    await ctx.respond(embed=help)


@client.slash_command(name="link-lol", guild_ids=[hearth],
                      description="Link To Your League Account")
async def link(ctx, name: discord.Option(str, description="Your Summoner Name", required=True)):
    await ctx.respond(bot.add_summoner(ctx.user, name))


@client.slash_command(name="pushup", guilt_ids=[hearth],
                      description="Do Pushups. Default is 10, Max is 25")
async def pushup(ctx, amount: discord.Option(int, description="Amount of Pushups Done", required=False, default=10)):
    if bot.is_pChat(ctx.channel):
        await ctx.respond(bot.pushup(ctx.user, amount))
    else:
        await ctx.respond("This isn't the channel for that!")

ops = ["Wins",
         "Losses",
         "Kills",
         "Deaths",
         "Most Kills in One Game",
         "Assists",
         "Pentas",
         "Quadras",
         "Games Played",
         "Win Streak",
         "Loss Streak"
         ]
boards = [discord.SelectOption(label=x,value=y) for x,y in zip(ops,sorts)]
class bView(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.delete()
    @discord.ui.select(placeholder="Choose a Leaderboard",min_values=1, max_values=1,options= boards)
    async def select_callback(self,select,interaction):
        await interaction.response.edit_message(embed = bot.leaderboard(select.values[0]))
@client.slash_command(name="lol-top", guild_ids=[hearth],
                      description="View League Leaderboards")
async def lol_top(ctx):
    await ctx.respond(embed=bot.leaderboard("l_wins"),view=bView(timeout=30))

@client.slash_command(name="random-quote", guild_ids=[hearth],
                      description="Read a Random Quote")
async def random_quote(ctx):
    global current_quiz, game_answer
    question = (bot.random_quote())
    game_answer= question[1]
    print(game_answer)
    current_quiz = await ctx.respond(f'{question[0]}')


@client.slash_command(name="answer", guild_ids=[hearth],
                      description="Answer a Quote Quiz")
async def ans(ctx, answer:discord.Option(discord.User, required = True,  description="Who said the quote")):
    player = ctx.user
    global game_answer
    if game_answer:
        if str(answer.id) in game_answer:
            await ctx.respond(f"✅{player.mention} Guessed The Quote!✅\nIt was {answer.mention}")
            game_answer = None
        else:
            await ctx.respond("❌Wrong Answer❌")
        print(answer.id)

    else:
        await ctx.respond("No games running")




@discord.ext.tasks.loop(minutes=5, reconnect=True)
async def lol_reload():
    pushup_channel = client.get_channel(hearth_p)
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"<{current_time}> Searching for Games...")
    reload = await bot.lol_reload()
    if reload:
        for x in reload:
            await pushup_channel.send(x)


@client.slash_command(name="test", guild_ids=[hearth])
async def test(ctx):
    print(ctx.user)
    print(ctx.channel)
    await ctx.respond("It Worked")


client.run(bot.TOKEN)
