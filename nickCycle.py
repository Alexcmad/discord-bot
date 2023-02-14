from tinydb import TinyDB, Query
import tinydb.operations as dbop

user_nicks = TinyDB("user_nick.json")
user = Query()
max_nicks = 5


def add_user(user_id):
    user_nicks.insert({'id': user_id, "nicks": [], "cycle": True, "idx": 0})


def is_user(user_id):
    if user_nicks.search(user.id == user_id):
        return
    else:
        add_user(user_id)
        return


def add_nick(user_id, nick: str):
    is_user(user_id)
    toggle(user_id)
    if len(get_nicks(user_id)) <= max_nicks:
        user_nicks.update(dbop.add("nicks", [nick]), user.id == user_id)

        return f"Nick {nick} added"
    else:
        return "You have the max amount of nicks already!"


def get_nicks(user_id):
    is_user(user_id)
    return user_nicks.search(user.id == user_id)[0]['nicks']


def remove_nick(user_id, nick: str):
    nick_list: list = get_nicks(user_id)
    if not nick_list:
        return "You have no nicks"
    for idx, n in enumerate([n.lower() for n in nick_list]):
        if n == nick.lower():
            nick = nick_list.pop(idx)
            user_nicks.update({'nicks': nick_list}, user.id == user_id)
            return f"{nick} removed from your list of nicks"
    return "Couldn't find that nick"


def cycle_nicks():
    user_nicks.update(dbop.increment("idx"), user.nicks != [])
    # user_nicks.update({"cycle": False}, user.nicks == [])
    to_update = []
    for i in user_nicks:
        idx = i["idx"]
        if len(i['nicks']) <= idx:
            idx = 0
            user_nicks.update({"idx":0},user.id == i['id'])
        if i["nicks"] and i["cycle"]:
            to_update.append((i['id'], get_nicks(i['id'])[idx]))

    return to_update


def toggle(user_id):
    is_user(user_id)
    if user_nicks.search(user.id == user_id)[0]['cycle']:
        user_nicks.update({'cycle': False}, user.id == user_id)
        return "Your nicks will no longer cycle"
    else:
        user_nicks.update({'cycle': True}, user.id == user_id)
        return "Your nicks will now cycle"


def remove_all(user_id):
    is_user(user_id)
    user_nicks.update({"nicks": []}, user.id == user_id)
    return "All nicks removed"
