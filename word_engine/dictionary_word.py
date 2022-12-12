import os
import re
from random import randint

dir_f = os.path.dirname(os.getcwd()) + '\\word-game\\word_engine\\singular.txt'


def read_dict():
    with open(f'{dir_f}', encoding='utf-8') as f:
        dicts = [i.lower().rstrip() for i in f.readlines()]
    return dicts


def update_dict(word):
    with open(f'{dir_f}', 'a', encoding='utf-8') as f:
        f.write(f'\n{word}')


def check_word(word) -> bool:
    if word in read_dict():
        return True
    else:
        return False


def get_words(word):
    letter = last_letter(word)
    regex = fr'{letter}.*'

    dict_curr_words = [i for i in read_dict() if re.match(regex, i)]
    return dict_curr_words


def return_word(word=None):
    if word is None:
        dirs = read_dict()
        return dirs[randint(0, len(dirs) - 1)]
    else:
        if check_word(word):
            try:
                dir_words = get_words(word)
                return dir_words[randint(0, len(dir_words) - 1)]
            except:
                pass
        else:
            return None
        # else:
        #     ask = input('add new word? y/n(д/н):')
        #     if ask in ('y', 'д', 'yes', 'да'):
        #         return check_add_word(word)
        #     else:
        #         return None


def check_add_word(word):
    update_dict(word)
    return return_word(word)


def check_typed_word(word):
    ...


def last_letter(word):
    # if isMatch()
    w = word[-1]
    if w in ('ь', 'ы', '.'):
        w = word[-2]
    return w


def isMatch(word_new,
            word=str | None):
    if word is None:
        return True

    w = last_letter(word)

    if w == word_new[0]:
        return True
    else:
        return False
