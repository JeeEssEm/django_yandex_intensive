def count_letters(value, alphabet):
    return sum(bool(s in alphabet) for s in value)


def is_english(value):
    eng = 'qwertyuiopasdfghjklzxcvbnm'
    rus = 'йцукенгшщзхъфывапролдэжячсмитьбюё'

    return count_letters(value, eng) > count_letters(value, rus)


def get_normalized(value):
    value = value.lower()
    similar_eng_symbols = [
        'a',
        'y',
        'o',
        'm',
        'p',
        'k',
        'b',
        'c',
        't',
        'h',
        'e'
    ]
    similar_rus_symbols = [
        'а',
        'у',
        'о',
        'м',
        'р',
        'к',
        'в',
        'с',
        'т',
        'н',
        'е'
    ]
    special_symbols = ',. '
    is_eng = is_english(value)
    res = ''

    for letter in value:
        if is_eng and letter in similar_rus_symbols:
            res += similar_eng_symbols[similar_rus_symbols.index(letter)]
        elif not is_eng and letter in similar_eng_symbols:
            res += similar_rus_symbols[similar_eng_symbols.index(letter)]
        elif letter not in special_symbols:
            res += letter

    return res
