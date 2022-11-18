from tinydb import TinyDB, Query
import tinydb.operations as dbop
import discord
import discord.ext.tasks
from riotwatcher import LolWatcher
from random import choice

import functools
import typing
import asyncio

colors = [0xFFE4E1, 0x00FF7F, 0xD8BFD8, 0xDC143C, 0xFF4500, 0xDEB887, 0xADFF2F, 0x800000, 0x4682B4, 0x006400, 0x808080,
          0xA0522D, 0xF08080, 0xC71585, 0xFFB6C1, 0x00CED1]


def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper


TOKEN = 'MTA0MDEyNTQ0MTQyOTczMzM3Ng.GSict-.sdYFNSpiPiTJVu33Ak2rcywbADqz3ukkETIOKg'
RIOT = 'RGAPI-a3d42d66-f154-43e8-885e-52a13c75809c'
region = 'NA1'
watcher = LolWatcher(api_key=RIOT)

db = TinyDB('userbase.json')

users = db.table('user_data')
User = Query()

guilds = db.table('server_data')
Server = Query()

pushupCount = 10


def is_user(user):
    if users.search(User.ID == get_ID(user)):
        # print(f"{get_name(user)}", end=' ')
        return
    else:
        print("User not Found. Adding.")
        users.insert(add_user(user))
        return


def add_user(user):
    return {'ID': get_ID(user),
            'name': get_name(user),
            'count': 0,
            'due': 0,
            'L': 0,
            'counted': 0,
            'quote': [],
            'pID': None,
            "l_max_kill": 0,
            "l_kills": 0,
            "l_deaths": 0,
            "l_wins": 0,
            "l_games": 0,
            "l_losses": 0,
            "l_win_streak": 0,
            "l_loss_streak": 0,
            "l_pentas": 0,
            "l_assists": 0,
            "l_quadras": 0
            }


def is_server(server):
    if guilds.search(Server.ID == get_ID(server)):
        return
    else:
        print(f"Adding new server {get_name(server)}")
        guilds.insert(add_server(server))


def add_server(server):
    return {'ID': get_ID(server),
            'name': get_name(server),
            'pChat': None,
            'cChat': None,
            'qChat': None
            }


def get_ID(obj):
    return obj.id


def get_name(obj):
    return obj.name


def take_L(user):
    try:
        is_user(user)
        users.update_multiple([
            (dbop.add('due', pushupCount), User.ID == get_ID(user)),
            (dbop.add('L', 1), User.ID == get_ID(user))])
        msg = f'{user.mention} Has to do {pushupCount} Pushups!'
        return msg
    except:
        ID = user.get('ID')
        users.update_multiple([
            (dbop.add('due', pushupCount), User.ID == ID),
            (dbop.add('L', 1), User.ID == ID)])
        msg = f'***🚨L DETECTED🚨*** \n<@{ID}> Has to do {pushupCount} Pushups!'
    print(f'{msg} THIS IS A BOT DETECTED L')
    return msg


def total_pushups(user):
    l = users.search(User.ID == get_ID(user))[0].get('count')
    return l


def due(user):
    l = users.search(User.ID == get_ID(user))[0].get('due')
    return l


def pushup(user, amount):
    if amount < 0:
        return "Bro tried to do Negative pushups yall laugh at this nigga"
    elif amount == 0:
        return "😐"
    elif amount > 25:
        return f"Sureeeee you did buddy I believe you **{amount} pUsHuPs AdDeD** See?"
    users.update_multiple([
        (dbop.add('count', amount), User.ID == get_ID(user)),
        (dbop.subtract('due', amount), User.ID == get_ID(user))
    ])
    if users.search(User.ID == get_ID(user))[0].get('due') < 0:
        users.update({'due': 0}, User.ID == get_ID(user))
    return f'{user.mention} did {amount} pushups!'


def total_L(user):
    l = users.search(User.ID == get_ID(user))[0].get('L')
    return l


def total_count(user):
    l = users.search(User.ID == get_ID(user))[0].get('counted')
    return l


def stats(user):
    is_user(user)
    embed = discord.Embed(title=f"{get_name(user)}'s Profile", colour=choice(colors))
    embed.add_field(name="Pushups Done", value=total_pushups(user), inline=False)
    embed.add_field(name="Pushups Due", value=due(user), inline=False)
    embed.add_field(name="L's", value=total_L(user), inline=False)
    embed.add_field(name="Times Counted", value=total_count(user), inline=False)
    embed.add_field(name="Random Quote", value=get_quote(user), inline=False)
    # l = f"{user.mention}'s Profile:\nTotal Pushups Done: {total_pushups(user)}\nL's Taken: {total_L(user)}\nTimes Counted: {total_count(user)}\nLatest Quote: {get_quote(user)}"
    # print(f"'s Profile: {l}")
    return embed


def set_pChat(channel, server):
    guilds.update({'pChat': get_ID(channel)}, Server.ID == get_ID(server))
    print(f"{get_name(channel)} set as pushup chat")
    return 'Current channel set as Pushup Chat'


def is_pChat(channel):
    if guilds.search(Server.pChat == get_ID(channel)):
        return True
    else:
        return False


def set_cChat(channel, server):
    guilds.update({'cChat': get_ID(channel)}, Server.ID == get_ID(server))
    print(f"{get_name(channel)} set as counting chat")
    return 'Current channel set as Count Chat'


def is_cChat(channel):
    if guilds.search(Server.cChat == get_ID(channel)):
        return True
    else:
        return False


def set_qChat(channel, server):
    guilds.update({'qChat': get_ID(channel)}, Server.ID == get_ID(server))
    print(f"{get_name(channel)} set as quote chat")
    return 'Current channel set as Quote Chat'


def is_qChat(channel):
    if guilds.search(Server.qChat == get_ID(channel)):
        return True
    else:
        return False


def get_qChat(server):
    l = guilds.search(Server.ID == get_ID(server))[0].get("qChat")
    return l


def counted(user):
    is_user(user)
    users.update(dbop.increment('counted'), User.ID == get_ID(user))
    print('Counted')
    return


def quote(message, user):
    is_user(user)
    users.update(dbop.add(('quote'), [f'_{message}_']), User.ID == get_ID(user))
    print(f'has a new Quote: {message}')


def get_quote(user):
    try:
        return choice(users.search(User.ID == get_ID(user))[0].get('quote'))
    except:
        return "Bro has no quotes 😐"


def add_summoner(user, summoner_name):
    is_user(user)
    try:
        pID = watcher.summoner.by_name(region=region, summoner_name=summoner_name)['puuid']
    except:
        return 'Something went wrong'

    users.update({'pID': pID}, User.ID == get_ID(user))
    return f'Successfully Linked to {summoner_name}'


def past_matches(user):
    userid = get_ID(user)
    pID = users.search(User.ID == userid)[0].get('pID')
    if not pID:
        return 'Not Linked to Riot'


def get_summoner(pID):
    return watcher.summoner.by_puuid(region=region, encrypted_puuid=pID)['name']


def get_level(pID):
    return watcher.summoner.by_puuid(region=region, encrypted_puuid=pID)['summonerLevel']

def get_usr_kda(user):
    return round(get_usr_kills(user) / get_usr_deaths(user),2)
def lol_stats(user):
    is_user(user)
    userid = get_ID(user)
    pID = users.search(User.ID == userid)[0].get('pID')
    if not pID:
        return f'Not Linked to Riot. \nDo:   .link lol [Summoner Name]'

    embed = discord.Embed(title=f"{get_name(user)}'s League Profile", colour=choice(colors))
    embed.add_field(name="Summoner Name", value=get_summoner(pID), inline=True)
    embed.add_field(name="Level", value=get_level(pID), inline=True)
    embed.add_field(name="Total Games🎮", value=get_usr_games(user), inline=True)

    #embed.add_field(name=u'\u200b', value=u'\u200b')
    embed.add_field(name="Wins🥇", value=get_usr_wins(user), inline=True)
    embed.add_field(name="Losses🥲", value=get_usr_losses(user), inline=True)
    embed.add_field(name="W/R Ratio", value=round(get_usr_wins(user)/get_usr_losses(user),2), inline=True)
    #embed.add_field(name=u'\u200b', value=u'\u200b')
    embed.add_field(name="K/D Ratio", value=get_usr_kda(user), inline=True)
    embed.add_field(name="Win Streak👑", value=get_usr_winstreak(user), inline=True)
    embed.add_field(name="Loss Streak🐵", value=get_usr_lossstreak(user), inline=True)
    #embed.add_field(name=u'\u200b', value=u'\u200b')
    embed.add_field(name="Kills🗡", value=get_usr_kills(user), inline=True)
    embed.add_field(name="Deaths⚰️", value=get_usr_deaths(user), inline=True)
    embed.add_field(name="Assists💖", value=get_usr_assists(user), inline=True)
    #embed.add_field(name=u'\u200b', value=u'\u200b')
    embed.add_field(name="Most Kills🔥", value=get_usr_max_kill(user), inline=True)
    embed.add_field(name="Pentas☠️", value=get_usr_pentas(user), inline=True)
    embed.add_field(name="Quadras😐", value=get_usr_quadras(user), inline=True)
    #embed.add_field(name=u'\u200b', value=u'\u200b')

    return embed


def get_last_game(pID):
    if not pID:
        return None

    return users.search(User.pID == pID)[0].get('l_game')


def get_last_20_game(pID):
    if not pID:
        return None

    lastGames = watcher.match.matchlist_by_puuid(region, pID)
    return lastGames


@to_thread
def lol_reload():
    list = []
    for user in users.all():
        if get_last_20_game(user['pID']):
            lastGame = get_last_20_game(user['pID'])[0]
        else:
            continue
        if lastGame == get_last_game(user['pID']):
            continue
        else:
            users.update({"l_game": lastGame}, user['ID'] == User.ID)
            print(f'New game found for {users.search(User.pID == user["pID"])[0].get("name")}')
            game = get_game(lastGame)
            player_update(game, user["pID"])
            player = get_player(game, user["pID"])
            if not get_win(player):
                list.append(take_L(user))
    return list


def update_20():
    users.update({"l_max_kill": 0,
                  "l_kills": 0,
                  "l_deaths": 0,
                  "l_wins": 0,
                  "l_games": 0,
                  "l_losses": 0,
                  "l_win_streak": 0,
                  "l_loss_streak": 0,
                  "l_pentas": 0,
                  "l_assists":0,
                  "l_quadras":0
                  })
    for user in users.all():

        pID = user['pID']
        if get_last_20_game(pID):
            lastGames = get_last_20_game(pID)
        else:
            continue
        for x in reversed(lastGames):
            game = get_game(x)
            player_update(game, pID)
    print("done")


def get_parts(game):
    return game['metadata']['participants']


def get_info(game):
    return game['info']['participants']


def get_player(game, pID):
    idx = get_parts(game).index(pID)
    player = get_info(game)[idx]
    return player


def get_kills(player):
    return player['kills']


def get_win(player):
    return player['win']


def get_deaths(player):
    return player['deaths']


def get_penta(player):
    return player['pentaKills']

def get_assist(player):
    return player['assists']

def get_quadras(player):
    return player['quadraKills']

def player_update(game, pID):
    player = get_player(game, pID)
    kills = get_kills(player)
    win = get_win(player)
    deaths = get_deaths(player)
    pentas = get_penta(player)
    assists = get_assist(player)
    quadra = get_quadras(player)

    users.update(dbop.add('l_kills', kills), User.pID == pID)
    users.update(dbop.add('l_deaths', deaths), User.pID == pID)
    users.update(dbop.add('l_pentas', pentas), User.pID == pID)
    users.update(dbop.add('l_quadras', quadra), User.pID == pID)
    users.update(dbop.add('l_assists', assists), User.pID == pID)
    users.update(dbop.increment('l_games'), User.pID == pID)

    if kills > users.search(User.pID == pID)[0].get('l_max_kill'):
        users.update({'l_max_kill': kills}, User.pID == pID)
    if win:
        users.update(dbop.increment('l_wins'), User.pID == pID)
        users.update(dbop.increment('l_win_streak'), User.pID == pID)
        users.update({'l_loss_streak': 0}, User.pID == pID)
    elif not win:
        users.update(dbop.increment('l_losses'), User.pID == pID)
        users.update({'l_win_streak': 0}, User.pID == pID)
        users.update(dbop.increment('l_loss_streak'), User.pID == pID)


def get_usr_kills(user):
    return users.search(User.ID == get_ID(user))[0].get('l_kills')


def get_usr_deaths(user):
    return users.search(User.ID == get_ID(user))[0].get('l_deaths')


def get_usr_wins(user):
    return users.search(User.ID == get_ID(user))[0].get('l_wins')


def get_usr_losses(user):
    return users.search(User.ID == get_ID(user))[0].get('l_losses')


def get_usr_winstreak(user):
    return users.search(User.ID == get_ID(user))[0].get('l_win_streak')


def get_usr_lossstreak(user):
    return users.search(User.ID == get_ID(user))[0].get('l_loss_streak')


def get_usr_pentas(user):
    return users.search(User.ID == get_ID(user))[0].get('l_pentas')


def get_usr_games(user):
    return users.search(User.ID == get_ID(user))[0].get('l_games')

def get_usr_assists(user):
    return users.search(User.ID == get_ID(user))[0].get('l_assists')

def get_usr_quadras(user):
    return users.search(User.ID == get_ID(user))[0].get('l_quadras')

def get_usr_max_kill(user):
    return users.search(User.ID == get_ID(user))[0].get('l_max_kill')


def get_game(game):
    return watcher.match.by_id(region, game)


def leaderboard(sort):
    playsLol = users.search((User.pID != None))
    list = sorted(playsLol, key=lambda d: d[sort], reverse=True)
    desc = {"l_wins": "***👑🥇Leaderboard of Wins🥇👑***",
            "l_kills": "***🗡️Leaderboard of Kills🗡️***",
            "l_deaths": "***☠️Leaderboard of Deaths☠️***",
            "l_pentas": "***🗡🗡🗡🗡🗡Leaderboard of Pentas🗡🗡🗡🗡🗡️***",
            "l_losses": "***😐Leaderboard of Losses😐***",
            "l_win_streak": "***🔥Leaderboard of Win Streaks🔥***",
            "l_loss_streak": "***😐Leaderboard of Loss Streaks😐***"
            ,"l_max_kill": "***🔥🗡️🔥Most Kills in One Game!🔥🗡️🔥***"
            ,"l_games": "***🎮Most Games Played🎮***"
        , "l_assists": "***💖Leaderboard of Assists💖***"
        , "l_quadras": "***💖🗡🗡🗡🗡Leaderboard of Quadras🗡🗡🗡🗡💖***"
            }
    board = discord.Embed(title=desc.get(sort), colour=choice(colors))
    board.set_footer(text="Use the menu to change Leaderboard Types")
    try:
        for pleb in range(9):
            pre = pleb + 1
            if pre in range(1, 4):
                if pre == 1:
                    pre = "👑🥇👑"
                elif pre == 2:
                    pre = "🥈"
                elif pre == 3:
                    pre = '🥉'

                board.add_field(name=f"{pre}{list[pleb].get('name')}{pre}", value=list[pleb].get(sort), inline=False)
            else:
                board.add_field(name=f"{list[pleb].get('name')}", value=list[pleb].get(sort), inline=True)
    except:
        return board
    return board

def random_quote():
    q = choice(choice(users.search(len(User.quote)>1)).get("quote"))
    if (q.split())>1:
        return q
    else:
        random_quote()
