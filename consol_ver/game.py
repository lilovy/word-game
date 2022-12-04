from word_engine.dictionary_word import last_letter, return_word, isMatch


def main():
    buffer = []
    buffer_bot = []
    word = return_word()
    while True:
        buffer_bot.append(word)
        print(word)
        x = input(f"input the word on '{last_letter(word)}', for exit push enter: ")
        if x in ('exit', ''):
            break
        if x == 'buf':
            print(buffer_bot)

        if isMatch(x, word) and x not in buffer:
            if x not in buffer_bot:
                word_backup = word
                if word is not None:
                    buffer.append(x)
                    word = return_word(x)
                if word == 'exit':
                    break
                if word is None:
                    word = word_backup
                    buffer.remove(x)
            else:
                print('dont repeat after the bot')
        elif x in buffer:
            print('this word was used later')
        else:
            print(f"incorrect word, type the word on '{last_letter(word)}'")


