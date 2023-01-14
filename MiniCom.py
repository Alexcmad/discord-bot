from random import choice

import discord
from tinydb import TinyDB, Query
import json
import tinydb.operations as dbop

import bot

colors = bot.colors
from discord import Embed

adult = 18


class Jobs:
    def __init__(self, db_file):
        self.db = TinyDB(db_file)
        self.job_data = self.db.table('job_data')
        self.Job = Query()

    def add_job(self, data):
        self.job_data.insert(data)
        return 'Job Added Successfully'

    def get_job(self, ID):
        return self.job_data.search(self.Job.id == ID)[0]

    def job_list(self):
        return self.job_data.all()


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
            char['health'] = 100 - decay  # Subtract decay from max health

            # add health benefit in the future

            if char.setdefault('alive', True):
                expenses = char.get('expenses', 0)
                income = char.get('income', 0)
                char['money'] = char['money'] - expenses + income
            self.update_player(char['id'], char)

            if char.get('health') <= 0 and char.get('alive'):
                notice.append(self.kill(char['id'], 'Old Age'))

            if char.get('age') >= adult and not char.get('adult', False):
                notice.append(self.adulthood(char['id']))

        return notice

    def kill(self, ID, method):
        means = method[0]
        self.update_player(ID, {'health': 0, 'alive': False})
        char = self.get_player(ID)['name']
        return f"{char} Has Died from {means}"

    def get_job(self, ID, job_ID):
        char = self.get_player(ID)
        job = jobs.get_job(job_ID)

        income = job.get('salary')
        name = job.get('name')

        if char['occupation']:
            return f'You are already a {name}'

        char['occupation'] = name
        char['income'] += income
        self.update_player(ID, char)
        return f"Congratulations! {char['name']} is now a {name}! +${income} Income"


players = Players(db_file='minicom.json')
jobs = Jobs(db_file='minicom.json')


def new_player(ID, name, gender):
    if players.get_player(ID):
        return 'You Already Have a Character'
    else:
        data = {'id': ID, 'name': name, 'age': 0,
                'adult': False, 'gender': gender,
                'money': 0, 'health': 100,
                'alive': True, 'occupation': None,
                'expenses': 0, 'income': 0}
        players.add_player(data)
        return f"Character {name} added Successfully"


def new_job(salary, name):
    ID = jobs.job_data.search(jobs.Job.current_id > -1)[0]['current_id']
    data = {'id': ID, 'name': name, 'salary': salary}
    jobs.job_data.update({'current_id': (ID + 1)}, jobs.Job.current_id > -1)
    jobs.add_job(data)


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
        embed.add_field(name='Health', value=round(health, 1))
        embed.add_field(name=u'\u200b', value=u'\u200b')
        embed.add_field(name='Money', value=f"${round(data['money'], 2)}")
        embed.add_field(name='Expenses', value=f"${data.get('expenses', 0)}")
        embed.add_field(name=u'\u200b', value=u'\u200b')

        return embed
    else:
        return "You don't have a Character made"
