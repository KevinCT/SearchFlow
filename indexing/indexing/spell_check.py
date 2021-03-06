from spellchecker import spellchecker

# Do spell check in a different thread
def spell_check_test():
    spell = SpellChecker()
    misspelled = spell.unknown(['jaka', 'is', 'hapenning', 'here'])
    start = time.time()
    syns = wordnet.synsets('car')
    end = time.time()
    print("first")
    print(end - start)

    for word in ['jaka', 'is', 'hapenning', 'here']:
        # Get the one `most likely` answer
        start = time.time()
        print(spell.correction(word))
        end = time.time()
        print("first")
        print(end - start)
        # Get a list of `likely` options

        start = time.time()
        print(spell.candidates(word))
        end = time.time()
        print("end")
        print(end - start)

    word_list = words.words()
    # prints 236736

    print(word_list.index('base'))

    # word_list.add(computer science terms)

