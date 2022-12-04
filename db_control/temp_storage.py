

buffer_user = {}

buffer_bot = {}

user_bases = {}


def fill_dict(userId, word, buff):
    buff.setdefault(userId, []).append(word)
