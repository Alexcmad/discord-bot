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
        self.health_decay = 0  # Will be subtracted from the player's health
        self.exponent = 1.05  # The exponent the Players' health deteriorates by with age
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
        try:
            self.db.remove(self.Player.id == ID)
            return "Character Deleted Successfully"
        except:
            return "You don't have a Character made"

    def get_player(self, ID):
        try:
            return self.db.search(self.Player.id == ID)[0]
        except:
            return 0

    def adulthood(self, ID):
        char = self.get_player(ID)
        self.update_player(ID, {'adult': True})
        self.update_player(ID, {'expenses': 100})
        return f"{char['name']} is now an adult! They will have to start paying for food. +$100 in expenses"

    def year(self):
        notice = []
        self.db.update(dbop.increment('age'), self.Player.health > 0)
        for char in self.db.all():
            char_exp = self.exponent ** char['age']  # Calculate the exponential value (age decay)
            decay = (char_exp + self.health_decay - 1.05)  # Calculate the total amount to subtract from health
            char['health'] = round(100 - decay, 1)  # Subtract decay from health and round to one decimal place

            expenses = char.setdefault('expenses', 0)
            income = char.setdefault('income', 0)
            char['money'] = char['money'] - expenses + income
            self.update_player(char['id'], char)

            if char['health'] <= 0 and char.setdefault('alive', True):
                notice.append(self.kill(char['id'], ['Old Age']))

            if char['age'] >= adult and not char.setdefault('adult', False):
                notice.append(self.adulthood(char['id']))

        return notice

    def kill(self, ID, method):
        means = method[0]
        self.update_player(ID, {'health': 0, 'alive': False})
        char = self.get_player(ID)['name']
        return f"{char} Has Died from {means}"

    """def deteriorate(self):
        self.db.update({'health':})"""


players = Players(db_file='minicom.json')


def new_player(ID, name, gender):
    if players.get_player(ID):
        return 'You Already Have a Character'
    else:
        data = {'id': ID, 'name': name, 'age': 0, 'gender': gender, 'money': 0, 'health': 100}
        players.add_player(data)
        return f"Character {name} added Successfully"


def view_player(ID):
    data = players.get_player(ID)
    if data:

        health = data['health']
        if health <= 0:
            health = 'Dead'

        embed = discord.Embed(title=f"Character Info", colour=choice(colors))
        embed.add_field(name='Name', value=data['name'])
        embed.add_field(name='Age', value=data['age'])
        embed.add_field(name=u'\u200b', value=u'\u200b')
        embed.add_field(name='Sex', value=data['gender'])
        embed.add_field(name='Health', value=health)
        embed.add_field(name=u'\u200b', value=u'\u200b')
        embed.add_field(name='Money', value=f"${data['money']}")
        embed.add_field(name='Expenses', value=f"${data.setdefault('expenses', 0)}")
        embed.add_field(name=u'\u200b', value=u'\u200b')

        return embed
    else:
        return "You don't have a Character made"
