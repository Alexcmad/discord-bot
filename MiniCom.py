from random import choice

import discord
from tinydb import TinyDB, Query
import json
import tinydb.operations as dbop

import bot

colors = bot.colors
from discord import Embed

adult = 18


class Players:
    def __init__(self, db_file):
        self.db = TinyDB(db_file)
        self.Player = Query()
        """ self.vehicles = []
        self.name = name
        self.age = 0
        self.balance = 0
        self.houses = []
        self.occupation = None
        self.owns = []
        self.parents = parents
        self.children = []
        self.nationality = nationality
        self.income = 0
        self.expenses = 0
        self.sex = sex"""

    def add_player(self, data):
        self.db.insert(data)

    def update_player(self, ID, new_data):
        self.db.update(new_data, self.Player.id == ID)

    def remove_Player(self, ID):
        self.db.remove(self.Player.id == ID)

    def get_player(self, ID):
        try:
            return self.db.search(self.Player.id == ID)[0]
        except:
            return 0

    def year(self):
        self.db.update(dbop.increment('age'))


players = Players(db_file='minicom.json')


def new_player(ID, name, gender):
    if players.get_player(ID):
        return '```You Already Have a Character```'
    else:
        data = {'id': ID, 'name': name, 'age': 0, 'gender': gender, 'money': 0, 'health': 100}
        players.add_player(data)
        return f"```Player {name} added Successfully```"


def view_player(ID):
    data = players.get_player(ID)
    print(data)
    if data:
        embed = discord.Embed(title=f"Character Info", colour=choice(colors))
        embed.add_field(name='Name', value=data['name'])
        embed.add_field(name='Age', value=data['age'])
        embed.add_field(name=u'\u200b', value=u'\u200b')
        embed.add_field(name='Sex', value=data['gender'])
        embed.add_field(name='Money', value=data['money'])
        embed.add_field(name=u'\u200b', value=u'\u200b')
        embed.add_field(name='Health', value=data['health'])

        return embed
    else:
        return "```You don't have a Character made```"


view_player(92)
