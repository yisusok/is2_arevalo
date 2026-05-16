import os

#*--------------------------------------------------------------------
#* Design pattern memento, ejemplo (Modificado para historial de 4 estados)
#*--------------------------------------------------------------------
class Memento:
    def __init__(self, file, content):
        self.file = file
        self.content = content


class FileWriterUtility:

    def __init__(self, file):
        self.file = file
        self.content = ""

    def write(self, string):
        self.content += string

    def save(self):
        return Memento(self.file, self.content)

    def undo(self, memento):
        self.file = memento.file
        self.content = memento.content


class FileWriterCaretaker:

    def __init__(self):
        self.history = []

    def save(self, writer):
        if len(self.history) == 4:
            self.history.pop(0)
        self.history.append(writer.save())

    def undo(self, writer, index=0):
        """
        index=0: Inmediato anterior
        index=1, 2, 3: Estados secuenciales más antiguos en el pasado
        """
        if not self.history:
            print("Historial vacío. No se puede deshacer.")
            return

        target_index = -1 - index

        try:
            memento = self.history[target_index]
            writer.undo(memento)
            print("<- Deshacer ejecutado exitosamente al nivel [{}] anterior ->".format(index))
        except IndexError:
            print("Error: No existe un estado tan antiguo en el historial (nivel {}).".format(index))


if __name__ == '__main__':

    os.system("clear")
    print("Crea un objeto que gestionará la versión anterior")
    caretaker = FileWriterCaretaker()

    print("Crea el objeto cuyo estado se quiere preservar")
    writer = FileWriterUtility("GFG.txt")

    print("Se graba algo en el objeto y se salva (Estado Histórico 3)")
    writer.write("Clase de IS2 en UADER\n")
    caretaker.save(writer)
    print(writer.content + "-----------------------------\n")

    print("Se graba información adicional y se salva (Estado Histórico 2)")
    writer.write("Material adicional de la clase de patrones\n")
    caretaker.save(writer)
    print(writer.content + "-----------------------------\n")

    print("Se graba información adicional II y se salva (Estado Histórico 1)")
    writer.write("Material adicional de la clase de patrones II\n")
    caretaker.save(writer)
    print(writer.content + "-----------------------------\n")

    print("Se graba información adicional III y se salva (Estado Inmediato Anterior [0])")
    writer.write("Material adicional de la clase de patrones III\n")
    caretaker.save(writer)
    print(writer.content + "-----------------------------\n")

    print("Se graba el Estado Actual de trabajo (No guardado aún)")
    writer.write("TEXTO ACTUAL FINAL\n")
    print(writer.content + "-----------------------------\n")

    
    # 1. Recuperamos el inmediato anterior (index=0)
    caretaker.undo(writer, 0)
    print("Estado actual:\n" + writer.content + "\n")

    # 2. Recuperamos el estado previo a ese (index=1)
    caretaker.undo(writer, 1)
    print("Estado actual:\n" + writer.content + "\n")

    # 3. Recuperamos el estado más antiguo guardado en la pila de 4 (index=3)
    caretaker.undo(writer, 3)
    print("Estado actual:\n" + writer.content + "\n")