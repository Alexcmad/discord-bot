import bot
import discord
import discord.ext.tasks
from riotwatcher import TftWatcher
from random import choice

import functools
import typing
import asyncio
region = bot.region
colors = bot.colors
watcher = TftWatcher(api_key=bot.RIOT)


def get_id(pID):
    return watcher.summoner.by_name(region=region, summoner_name=pID)


def get_rank(pID):
    pass


