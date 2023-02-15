class ReverseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.count = 0

    def __call__(self, request):
        alphabet = 'йцукенгшщзхъфывапролджэячсмитьбюё'
        response = self.get_response(request)

        self.count += 1

        if self.count == 10:
            self.count = 0
            text = response.getvalue().decode()
            word = ''
            for i, symbol in enumerate(text):
                if symbol.lower() in alphabet:
                    word += symbol
                elif word:
                    text = text[:i - len(word)] + word[::-1] + text[i:]
                    word = ''
            response.content = bytes(text, encoding='utf-8')

        return response
