class Observer:
    def update(self, emitted_id: str):
        pass


class IdConcreteObserver(Observer):
    def __init__(self, observer_id: str):
        self.id = observer_id

    def update(self, emitted_id: str):
        if self.id == emitted_id:
            print(f"[Match] Clase con ID '{self.id}' detectó su secuencia coincidente.")


class IdEmitter:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def emit(self, emitted_id: str):
        print(f"Emitiendo ID: {emitted_id}")
        for observer in self._observers:
            observer.update(emitted_id)


emitter = IdEmitter()

obs1 = IdConcreteObserver("A1B2")
obs2 = IdConcreteObserver("C3D4")
obs3 = IdConcreteObserver("E5F6")
obs4 = IdConcreteObserver("G7H8")

emitter.attach(obs1)
emitter.attach(obs2)
emitter.attach(obs3)
emitter.attach(obs4)

ids_a_emitir = ["A1B2", "XXXX", "C3D4", "YYYY", "E5F6", "ZZZZ", "G7H8", "W0W0"]

for current_id in ids_a_emitir:
    emitter.emit(current_id)
    print("-" * 40)