class Handler:
    def __init__(self, successor=None):
        self._successor = successor

    def handle(self, number, consumed_by):
        if self._successor:
            return self._successor.handle(number, consumed_by)
        return consumed_by


class PrimeHandler(Handler):
    def _is_prime(self, n):
        if n < 2: return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0: return False
        return True

    def handle(self, number, consumed_by):
        if self._is_prime(number):
            consumed_by.append("Primo")
        return super().handle(number, consumed_by)


class EvenHandler(Handler):
    def handle(self, number, consumed_by):
        if number % 2 == 0:
            consumed_by.append("Par")
        return super().handle(number, consumed_by)


chain = PrimeHandler(EvenHandler())

for num in range(1, 101):
    consumers = []
    chain.handle(num, consumers)
    
    if consumers:
        print(num, f"-> Consumido como: {', '.join(consumers)}")
    else:
        print(num, "-> No consumido")