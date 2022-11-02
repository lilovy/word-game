from dictionary_word import last_letter, return_word, isMatch


def main():
    buffer = []
    word = return_word()
    while True:
        print(word)
        x = input(f"input the word on '{last_letter(word)}', for exit input 'exit': ")
        if x == 'exit':

            break

        if isMatch(x, word) and x not in buffer:
            if word is not None:
                buffer.append(x)
                word = return_word(x)
            elif word is None:
                ...
        elif x in buffer:
            print('this word was used later')
        else:
            print(f"incorrect word, type the word on '{last_letter(word)}'")