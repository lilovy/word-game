from word_engine.dictionary_word import last_letter, return_word


def game(word=None):
    results = return_word()
    if results:
        return return_word(word)
    # else:


def last_ltr(word):
    return last_letter(word)
