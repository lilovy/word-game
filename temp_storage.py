

buffer_user = {}

buffer_bot = {}

user_bases = {}


def fill_dict(userId, word, buff):
    buff.setdefault(userId, []).append(word)


# def user_base(userId, username):
#     user_bases.setdefault(userId, []).append(u)



# fill_dict(1242342, 'word', buffer_user)
# fill_dict(1242342, 'back', buffer_user)
# fill_dict(1242332, 'top', buffer_user)
# fill_dict(1242342, 'lock', buffer_user)
# print(buffer_user[1242342])

