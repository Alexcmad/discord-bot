from random import choice
from tinydb import TinyDB, Query
import json
import tinydb.operations as dbop

db = TinyDB('minicom.json')
characters = db.table('player_data')
player = Query()

adult = 18


class Person:
    def __init__(self, name, parents, nationality, sex):
        self.vehicles = []
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
        self.sex = sex

    def grow(self):
        self.age += 1
        self.balance += self.income
        self.balance -= self.expenses
        if self.age == 18:
            return ("You're a grown up now! You have to find your own food! +$200 expenses")

    def buy(self, product):
        if self.balance >= product.price:
            self.balance -= product.price
            if type(product) == Building:
                self.houses.append(product)
            elif type(product) == Vehicle:
                self.vehicles.append(product)
            self.owns.append(product)
        else:
            return "Not Enough Money"

    def get_job(self, job):
        if self.age < adult:
            return "Too Young to work!"
        else:
            self.income += 10000
            return "You're Hired! +$10,000 income"

    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))


    def __str__(self):
        return f"{self.name}({self.age})({self.sex})\nOccupation: {self.occupation}\nBal: ${self.balance}\nHouses: {self.houses}"


class Item:
    def __init__(self, price, typ):
        self.price = price
        self.typ = typ

    def __str__(self):
        return f"{self.typ}\n${self.price}\n${self.price}"


class Asset(Item):
    def __init__(self, price, expense, typ):
        super().__init__(price, typ)
        self.expense = expense


class Building(Asset):
    def __init__(self, price, city, expense, country, description, typ):
        super().__init__(price=price, expense=expense, typ=typ)
        self.city = city
        self.country = country
        self.description = description

    def __str__(self):
        return f"{self.description}\n${self.price}\nLocation: {self.city},{self.country}"


class Vehicle(Asset):
    def __init__(self, price, brand, color, model, expense, typ):
        super().__init__(price, expense, typ)
        self.brand = brand
        self.color = color
        self.model = model


class Player(Person):
    def __init__(self, name, parents, nationality, sex,ID):
        super().__init__(name, parents, nationality, sex)
        self.ID = ID


def random_character(ID):
    names = ["Bob", "Alex", "Regina", "Mike"]
    name = choice(names)

    countries = ["JA", "USA", "SPN", 'UK', "GER"]
    nationality = choice(countries)

    parentals = [("Harry", "Carrie"), ("James", "Jane")]
    parents = choice(parentals)

    sexes = ("M", "F")
    sex = choice(sexes)

    character = Player(name=name, parents=parents, sex=sex, nationality=nationality, ID=ID)
    characters.insert(character.toJSON())
    return start(character)


def start(character):
    name = character.name
    nationality = character.nationality
    mother = character.parents[1]
    father = character.parents[0]
    return f"You are born as {name} in {nationality} and your parents are {mother} and {father}.\nCurrent age: 0"


def view_stats(ID):
    char = characters.search(player.ID == ID)
    if char:
        return(char[0])
    else:
        return "Not In Database"



