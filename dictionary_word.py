from random import randint
import re


def read_dict():
    with open('nouns.txt') as f:
        dicts = [i.lower().rstrip() for i in f.readlines()]
    return dicts


def update_dict(word):
    with open('nouns.txt', 'a') as f:
        f.write(f'\n{word}')


def check_word(word) -> bool:
    if word in read_dict():
        return True
    else:
        return False


def get_words(word):
    letter = word[-1]
    if word[-1] == 'ь':
        letter = word[-2]
    regex = fr'{letter}.*'

    dict_curr_words = [i for i in read_dict() if re.match(regex, i)]
    return dict_curr_words


def return_word(word=None):
    if word is None:
        dirs = read_dict()
        return dirs[randint(0, len(dirs)-1)]
    else:
        if check_word(word):
            try:
                dir_words = get_words(word)
                return dir_words[randint(0, len(dir_words)-1)]
            except:
                pass
        else:
            ask = input('add new word? y/n(д/н):')
            if ask in ('y', 'д', 'yes', 'да'):
                update_dict(word)
                return return_word(word)
            if ask in ('n', 'no', 'н', 'нет'):
                return None


def check_typed_word(word):
    ...


def last_letter(word):
    w = word[-1]
    if w == 'ь':
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





