class StringAggregate:
    def __init__(self, text: str):
        self.text = text

    def get_direct_iterator(self):
        return DirectIterator(self.text)

    def get_reverse_iterator(self):
        return ReverseIterator(self.text)


class DirectIterator:
    def __init__(self, text):
        self._text = text
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._text):
            char = self._text[self._index]
            self._index += 1
            return char
        raise StopIteration


class ReverseIterator:
    def __init__(self, text):
        self._text = text
        self._index = len(text) - 1

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= 0:
            char = self._text[self._index]
            self._index -= 1
            return char
        raise StopIteration


texto = StringAggregate("Patron")

print("Directo:", end=" ")
for char in texto.get_direct_iterator():
    print(char, end=" ")

print("\nReverso:", end=" ")
for char in texto.get_reverse_iterator():
    print(char, end=" ")
print()