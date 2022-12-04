import re
from word_engine.dictionary_word import read_dict


def add_word(word, folder='f_words.txt'):
    with open(folder, 'a') as f:
        f.write(f'{word}\n')


def filter_word(mask='.*ый'):
    regex = fr'{mask}'
    dict_curr_words = [i for i in read_dict() if not re.match(regex, i)]
    return dict_curr_words


def filtering():
    masks = fr".*ый\b|.*ий\b|.*ыйся\b|.*ийся\b|.*ться\b|.*тся\b|.*ать\b|.*ить\b|.*ыть\b|.*оть\b|.*уть\b|.*еть\b|.*ть\b"
    dct = filter_word(masks)
    for word in dct:
        add_word(word)
    # return dct


# filtering()
