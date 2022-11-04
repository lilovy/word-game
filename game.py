from dictionary_word import last_letter, return_word, isMatch


def main():
    buffer = []
    buffer_bot = []
    word = return_word()
    while True:
        buffer_bot.append(word)
        print(word)
        x = input(f"input the word on '{last_letter(word)}', for exit input 'exit': ")
        if x == 'exit':

            break

        if isMatch(x, word) and x not in buffer:
            word_backup = word
            if word is not None:
                buffer.append(x)
                word = return_word(x)
            if word is None:
                word = word_backup
                buffer.remove(x)
        elif x in buffer or x in buffer_bot:
            print('this word was used later')
        else:
            print(f"incorrect word, type the word on '{last_letter(word)}'")