from python_aternos import Client
import python_aternos as PA
from discord import Embed
from random import choice

colors = [0xFFE4E1, 0x00FF7F, 0xD8BFD8, 0xDC143C, 0xFF4500, 0xDEB887, 0xADFF2F, 0x800000, 0x4682B4, 0x006400, 0x808080,
          0xA0522D, 0xF08080, 0xC71585, 0xFFB6C1, 0x00CED1]

username = 'otherAlexcmad'
passcode = 'qu@6A86UWA@ck4S'

at = Client.from_credentials(username=username, password=passcode)

server = at.list_servers()[0]


def players():
    n = server.players_count
    if n:
        return f"`Online: {n} of {server.slots} players\n{server.players_list}`"
    else:
        return f"`Online: {n} of {server.slots} players`"


def start():
    try:
        server.start()
        return "`Starting Server...`"
    except PA.ServerStartError as err:
        return f"`{err.MESSAGE}`"


def restart():
    try:
        server.restart()
        return "`Restarting Server...`"
    except PA.ServerStartError as err:
        return f"`{err.MESSAGE}`"


def get_ip():
    return f"`{server.domain}`"


def get_version():
    return f"`{server.version}`"


def status():
    return f"`{server.status}`"


def player_list():
    lst = ''
    if server.players_list:
        for player in server.players_list:
            lst += player + '\n'
        return f"`{lst}`"
    else:
        return "`Nobody Online`"


def info():
    server.fetch()
    embed = Embed(title="Server Info", colour=choice(colors))
    embed.add_field(name='Server IP', value=get_ip(), inline=False)
    embed.add_field(name='Server Status', value=status(), inline=False)
    embed.add_field(name='Server Version', value=get_version(), inline=False)
    embed.add_field(name='Modpack', value='StoneBlock Modpack on CurseForge', inline=False)
    embed.add_field(name='Player Count', value=players(), inline=False)
    embed.add_field(name='Player List', value=player_list())

    return embed
