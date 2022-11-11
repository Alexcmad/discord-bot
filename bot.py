from tinydb import TinyDB, Query
import tinydb.operations as dbop
import discord


TOKEN='MTA0MDEyNTQ0MTQyOTczMzM3Ng.GSict-.sdYFNSpiPiTJVu33Ak2rcywbADqz3ukkETIOKg'

db = TinyDB('userbase.json')

users = db.table('user_data')
User = Query()

guilds = db.table('server_data')
Server = Query()

pushupCount = 10


def is_user(user):
    if users.search(User.ID == get_ID(user)):
        print(f"{get_name(user)}",end =' ')
        return
    else:
        print("User not Found. Adding.")
        users.insert(add_user(user))
        return


def add_user(user):
    return {'ID': get_ID(user),
            'name': get_name(user),
            'count': 0,
            'L': 0,
            'counted': 0,
            'quote':None}


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
    is_user(user)
    users.update_multiple([
        (dbop.add('count', pushupCount), User.ID == get_ID(user)),
        (dbop.add('L', 1), User.ID == get_ID(user))])
    msg = f'{user.mention} has to do {pushupCount} pushups!'
    print("Took an L")
    return msg


def total_pushups(user):
    l = users.search(User.ID == get_ID(user))[0].get('count')
    return l


def total_L(user):
    l = users.search(User.ID == get_ID(user))[0].get('L')
    return l

def total_count(user):
    l = users.search(User.ID == get_ID(user))[0].get('counted')
    return l


def stats(user):
    is_user(user)
    embed = discord.Embed(title=f"{get_name(user)}'s Profile")
    embed.add_field(name="Pushups Done", value=total_pushups(user), inline=False)
    embed.add_field(name="L's", value=total_L(user), inline=False)
    embed.add_field(name = "Times Counted", value= total_count(user), inline=False)
    embed.add_field(name = "Latest Quote", value=get_quote(user), inline=False)
    l = f"{user.mention}'s Profile:\nTotal Pushups Done: {total_pushups(user)}\nL's Taken: {total_L(user)}\nTimes Counted: {total_count(user)}\nLatest Quote: {get_quote(user)}"
    print(f"'s Profile: {l}")
    return embed


def set_pChat(channel, server):
    guilds.update({'pChat':get_ID(channel)}, Server.ID==get_ID(server))
    print(f"{get_name(channel)} set as pushup chat")
    return 'Current channel set as Pushup Chat'

def is_pChat(channel):
    if guilds.search(Server.pChat==get_ID(channel)):
        return True
    else:
        return False

def set_cChat(channel, server):
    guilds.update({'cChat':get_ID(channel)}, Server.ID==get_ID(server))
    print(f"{get_name(channel)} set as counting chat")
    return 'Current channel set as Count Chat'

def is_cChat(channel):
    if guilds.search(Server.cChat==get_ID(channel)):
        return True
    else:
        return False


def set_qChat(channel,server):
    guilds.update({'qChat': get_ID(channel)}, Server.ID == get_ID(server))
    print(f"{get_name(channel)} set as quote chat")
    return 'Current channel set as Quote Chat'

def is_qChat(channel):
    if guilds.search(Server.qChat==get_ID(channel)):
        return True
    else:
        return False

def get_qChat(server):
    l = guilds.search(Server.ID==get_ID(server))[0].get("qChat")
    return l

def counted(user):
    is_user(user)
    users.update(dbop.increment('counted'), User.ID == get_ID(user))
    print('Counted')
    return

def quote(message,user):
    is_user(user)
    users.update({'quote':f'_{str.title(message)}_'},User.ID==get_ID(user))
    print(f'has a new Quote: {message}')

def get_quote(user):
    return users.search(User.ID==get_ID(user))[0].get('quote')

