import asyncio
import datetime
import time
from random import choice
import random
import discord
from discord.ext import commands
import bot
import spotify
import nacl
import youtube_dl
import ffmpeg

intents = discord.Intents.all()
intents.voice_states = True
intents.guilds = True
client = commands.Bot(intents=intents)
lastMessage = None
edited = False
current_audio = None
moreCount = 0
game_answer = None
secs = 3
playlist = None
hearth = 695056946616860729
hearthGeneral = 742448286702633092
hearthManga = 1023978024359702591
bird = 229401751281729536
alex = 298206761587048448
tiff = 266656358512852992
doss = 316004737692598272
prefix = '.'
imgUrl = "https://ondemand.bannerbear.com/simpleurl/3vaNyD8JRLy8Ag0Q9L/image"
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
         "l_loss_streak",
         "guessed_songs",
         "count",
         "counted"
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
help.add_field(name="Join VC", value='/join', inline=False)
help.add_field(name="Play Guess The Song", value='/play [spotify playlist link] [optional amount of seconds]',
               inline=False)
help.add_field(name="Guess the song", value='/guess [song name] (you need to get at least 2/3 of the name)',
               inline=False)
help.add_field(name="Play more of the song if you cant guess", value='/more', inline=False)
help.add_field(name="Play another Round", value='/next-round', inline=False)
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
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Hentai"))

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
                print("Done")

        if msg.startswith((f'{prefix}manga')):
            print("Loading Manga...")
            async for x in channel.history():
                bot.load_manga(x.content, x.author.mention)
            print("Done")

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
       "Loss Streak",
       "Guessed Songs",
       "Pushups Done",
       "Times Counted"
       ]
boards = [discord.SelectOption(label=x, value=y) for x, y in zip(ops, sorts)]


class bView(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.delete()

    @discord.ui.select(placeholder="Choose a Leaderboard", min_values=1, max_values=1, options=boards)
    async def select_callback(self, select, interaction):
        await interaction.response.edit_message(embed=bot.leaderboard(select.values[0]))


@client.slash_command(name="lol-top", guild_ids=[hearth],
                      description="View League Leaderboards")
async def lol_top(ctx):
    await ctx.respond(embed=bot.leaderboard("l_wins"), view=bView(timeout=30))


@client.slash_command(name="random-quote", guild_ids=[hearth],
                      description="Read a Random Quote")
async def random_quote(ctx):
    global current_quiz, game_answer
    question = (bot.random_quote())
    game_answer = question[1]
    print(game_answer)
    current_quiz = await ctx.respond(f'{question[0]}')


@client.slash_command(name="answer", guild_ids=[hearth],
                      description="Answer a Quote Quiz")
async def ans(ctx, answer: discord.Option(discord.User, required=True, description="Who said the quote")):
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


@client.slash_command(name="guess", guild_ids=[hearth],
                      description="Guess the Song")
async def ans(ctx, answer: discord.Option(str, required=True, description="Name of The Song")):
    player = ctx.user
    global game_answer, current_audio
    if game_answer and current_audio:
        if str.upper(answer) in str.upper(game_answer[0]) and len(answer) > (len(game_answer[0].split('(')[0]) / 2):
            await ctx.respond(f"✅{player.mention} Guessed The Song!✅\nIt was {game_answer[0]} - {game_answer[1]}")
            current_audio = None
            game_answer = None
            bot.guessed(player)
        else:
            await ctx.respond("❌Wrong Answer❌")
        print(game_answer)

    else:
        await ctx.respond("No games running")


@client.slash_command(name="play", guild_ids=[hearth],
                      description="Try to guess the name of a random song from a spotify playlist")
async def play(ctx, playlist_link: discord.Option(str, required=True, description="Playlist Link"),
               seconds: discord.Option(int, required=False,
                                       description="The amount of seconds to play (default: 5, max: 10)", default=5)):
    global game_answer, playlist, secs, moreCount
    moreCount = 0
    secs = seconds
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format': "m4a/bestaudio/mp4/mp3", 'noplaylist': 'True', 'postprocessors':
        [{'key': 'FFmpegExtractAudio',
          'preferredcodec': 'm4a'}]}
    vc = None

    if ctx.user.voice:
        v_channel = ctx.user.voice.channel
        if not ctx.voice_client:
            await ctx.respond("connect with /join")
        else:
            vc = ctx.voice_client

            playlist = spotify.get_playlist_items(playlist_link)
            playlist_name = spotify.get_playlist_name(playlist_link)
            playlist_owner = spotify.get_playlist_owner(playlist_link)
            playlist_description = spotify.get_playlist_description(playlist_link)

            async def play_rand():
                vc.volume = .40
                global game_answer, current_audio
                song = spotify.get_track(choice(playlist))
                songName = spotify.get_track_name(song)
                songArtist = spotify.get_artist(song)
                game_answer = [songName, songArtist]

                await ctx.respond(
                    f"{ctx.user.mention} Started a guess the song from {playlist_name}\nAnswer with /guess [song name]\nFirst to answer Wins!")
                with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(f"ytsearch: {songName} {songArtist} lyrics", download=False)['entries'][0]
                    url2 = info['url']
                    current_audio = source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                    vc.play(source=source, after=lambda e: print('done', e))
                    await ctx.send(
                        "What is that ***MELODY?***\nhttps://tenor.com/view/creepy-what-is-the-melody-gif-19298771")
                    await asyncio.sleep(seconds)
                    vc.pause()
                    print(vc.is_playing())

            try:
                await play_rand()
            except:
                await ctx.respond("That Song Can't be played, try again")
    else:
        await ctx.respond(no_vc())


@client.slash_command(name="next-round", guild_ids=[hearth],
                      description="Play another round of guess the song with the current playlist")
async def next(ctx):
    global playlist, moreCount
    moreCount = 0

    if playlist:
        await ctx.respond("Next Round!")
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}
        YDL_OPTIONS = {'format': "m4a/bestaudio/mp4/mp3", 'noplaylist': 'True', 'postprocessors':
            [{'key': 'FFmpegExtractAudio',
              'preferredcodec': 'm4a'}]}
        vc = None

        if ctx.user.voice:
            v_channel = ctx.user.voice.channel
            if not ctx.voice_client:
                await ctx.respond("connect with /join")
            else:
                vc = ctx.voice_client

                async def play_rand():
                    global game_answer, current_audio
                    song = spotify.get_track(choice(playlist))
                    songName = spotify.get_track_name(song)
                    songArtist = spotify.get_artist(song)
                    game_answer = [songName, songArtist]

                    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                        vc.volume = .40
                        info = ydl.extract_info(f"ytsearch: {songName} {songArtist} lyrics", download=False)['entries'][
                            0]
                        url2 = info['url']
                        current_audio = source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                        vc.play(source=source, after=lambda e: print('done', e))
                        await ctx.send("What is that ***MELODY?***")
                        await asyncio.sleep(secs)
                        vc.pause()
                        print(vc.is_playing())

                try:
                    await play_rand()
                except:
                    await ctx.respond("That Song Can't be played, try again")
        else:
            await ctx.respond(no_vc())
    else:
        await ctx.respond("No game running")


@client.slash_command(name="more", guild_ids=[hearth],
                      description="Play more of the song")
async def more(ctx):
    global playlist, moreCount, current_audio
    moreNum = 5
    if moreCount >= 3:
        await ctx.respond(f"OMG UR SO DUMB it was {game_answer[0]} 🐒🐵🐒🙊🙈🙉🐒")
        ctx.voice_client.stop()
        current_audio = None
        moreCount = 0

    else:
        if moreCount == 1:
            moreNum = 10
        elif moreCount == 2:
            moreNum = 15

        if playlist and ctx.voice_client.is_paused():
            await ctx.respond(f"Playing {moreNum} more seconds...")

            if ctx.user.voice:
                v_channel = ctx.user.voice.channel
                if not ctx.voice_client:
                    await ctx.respond("connect with /join")
                else:
                    vc = ctx.voice_client
                    vc.volume = .40
                    vc.resume()
                    await ctx.send("What is that ***MELODY?***")
                    await asyncio.sleep(moreNum)
                    vc.pause()
                    print(vc.is_playing())
            else:
                await ctx.respond(no_vc())
            moreCount += 1
        elif ctx.voice_client.is_playing():
            await ctx.respond("Wait until the current song stops playing")
        else:
            await ctx.respond("No game running")


@client.slash_command(name="join", guild_ids=[hearth],
                      description="Let bot join a vc")
async def join(ctx):
    vc = None

    if ctx.user.voice:
        v_channel = ctx.user.voice.channel
        if not ctx.voice_client:
            await v_channel.connect(timeout=10)
            await ctx.respond("I'm in.")
        else:
            await ctx.respond("I'm already in.")
    else:
        await ctx.respond(no_vc())


def no_vc():
    return "Get in a VC first"


def same_vc():
    return "You need to be in the same VC as the bot to do this"


@client.slash_command(name="disconnect", guild_ids=[hearth],
                      description="disconnect the bot from vc")
async def disconnect(ctx):
    vc = ctx.voice_client
    if vc:
        if ctx.user.voice.channel == vc.channel:
            vc.cleanup()
            await vc.disconnect()
            await ctx.respond("Disconnected")
        else:
            await ctx.respond(same_vc())
    else:
        await ctx.respond("Bot Aint even Connected")


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


@client.event
async def on_voice_state_update(member, before, after):
    general = client.get_channel(hearthGeneral)
    if member.id == tiff:
        if after.channel and not before.channel:
            await general.send('https://tenor.com/view/tiffany-adonis-otogari-adonis-enstars-gif-19915582')
            await general.send('https://tenor.com/view/guilty-gear-may-tiff-skroup-gif-24321805')
        elif not after.channel:
            await general.send(
                'https://tenor.com/view/i-just-wish-tiff-were-here-brendan-scannell-pete-bonding-i-want-to-see-tiff-gif-16542187')
            await general.send(
                'https://tenor.com/view/tiffany-lupels-lupels-tiffany-tiffany-of-lopels-tiffany-of-lupelz-gif-14921736')
        elif before.channel and after.channel and after.self_mute and not before.self_mute:

            await general.send('https://tenor.com/view/tyra-banks-be-quiet-tiffany-bye-gif-8741675')

    if member.id == bird:
        if after.channel and not before.channel:
            await asyncio.sleep(1)
            vc = await after.channel.connect(timeout=2)
            filet = random.randint(0, 4)
            file = discord.FFmpegPCMAudio(f'Suck yuh modda ({filet}).m4a')
            vc.play(file)
            if filet != 4:
                await asyncio.sleep(2.5)
            else:
                await asyncio.sleep(7)
            await vc.disconnect()
    if member.id == doss:
        if after.channel and not before.channel:
            await general.send("Beighbeigh")


@client.slash_command(name="manga-list", guild_ids=[hearth],
                      description='Manga List')
async def manga_list(ctx):
    await ctx.respond(embed =bot.list_manga())


@client.slash_command(name="add-manga", guild_ids=[hearth],
                      description='Add manga to the list')
async def add_manga(ctx, title: discord.Option(str, name = 'title', required = True)):
    await ctx.respond(bot.add_manga(title, ctx.author.mention))


@client.slash_command(name="manga", guild_ids=[hearth],
                      description='random manga')
async def manga_list(ctx):
    await ctx.respond(embed =bot.random_manga())


@client.event
async def on_message_delete(message):
    global lastMessage, edited
    lastMessage = message
    edited = False


"""
@client.event
async def on_message_edit(before, after):
    global lastMessage, edited
    lastMessage = before
    edited = True
"""

@client.slash_command(name='snipe', guild_ids=[hearth],
                      description="Catch someone lackin'")
async def snipe(ctx):
    if lastMessage and not edited:
        user = lastMessage.author
        name = "+".join(user.name.split())
        raw_message = lastMessage.content.split()
        message = "+".join(raw_message)
        await ctx.respond(
            f"{imgUrl}/username/text/{name}/message/text/{message}/profile_pic/image_url/{lastMessage.author.avatar}")
    else:
        await ctx.respond("Nothing to Snipe")

"""
@client.slash_command(name='esnipe', guild_ids=[hearth],
                      description="Catch someone lackin'")
async def snipe(ctx):
    if lastMessage and edited:
        user = lastMessage.author
        name = "+".join(user.name.split())
        raw_message = lastMessage.content.split()
        message = "+".join(raw_message)
        await ctx.respond(
            f"{imgUrl}/username/text/{name}/message/text/{message}/profile_pic/image_url/{lastMessage.author.avatar}")
    else:
        await ctx.respond("Nothing to Snipe")
"""

client.run(bot.TOKEN)
