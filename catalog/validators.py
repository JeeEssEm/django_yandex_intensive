import re

import django.core.exceptions
import django.utils.deconstruct


@django.utils.deconstruct.deconstructible
class ValidateMustContain:
    def __init__(self, *perfect_words):
        self._perfect_words = perfect_words

    def __call__(self, val):
        open_tag = '<[^>]*>'
        close_tag = r'</[^>]*>'

        val = re.sub(open_tag, '', val[::])
        val = re.sub(close_tag, '', val[::])

        if not any(bool(re.match(rf'\b{word}\b', val)) for word
                   in self._perfect_words):
            raise django.core.exceptions.ValidationError(
                f'В тексте должно быть слово'
                f' {" или ".join(self._perfect_words)}'
            )
