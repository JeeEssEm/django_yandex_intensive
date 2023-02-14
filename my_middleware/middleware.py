def reverse_middleware(get_response):
    count = 1

    def middleware(request):
        nonlocal count
        alphabet = 'йцукенгшщзхъфывапролджэячсмитьбюё'
        response = get_response(request)

        if count % 10 == 0:
            text = response.getvalue().decode()
            word = ''
            for i, symbol in enumerate(text):
                if symbol.lower() in alphabet:
                    word += symbol
                elif word:
                    text = text[:i - len(word)] + word[::-1] + text[i:]
                    word = ''

            response.content = bytes(text, encoding='utf-8')

        count += 1
        return response

    return middleware
