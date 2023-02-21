import django.core.exceptions


def contains_perfect_words(val):
    perf_word = ['превосходно', 'роскошно']

    if not any(word in val for word in perf_word):
        raise django.core.exceptions.ValidationError(
            f'В тексте должно быть слово {" или ".join(perf_word)}'
        )
