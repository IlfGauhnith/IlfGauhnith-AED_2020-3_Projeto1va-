# CUSTOM EXCEPTIONS
class ChaveJaExiste(Exception):
    def __init__(self):
        self.message = 'Essa chave já existe na lista'

    def __str__(self):
        return f'Regra de chave única violada: {self.message}'


class ChaveInexistente(Exception):
    def __init__(self):
        self.message = 'Chave não existe na lista'

    def __str__(self):
        return f'{self.message}'


class FilaUnderflow(Exception):
    def __init__(self):
        self.message = 'Underflow!'

    def __str__(self):
        return f'Lista vazia: {self.message}'


class NoFilaSequencial:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class FilaSequencial:
    def __init__(self, tam):
        self.tam_max = tam
        self.fila = []
        self.last_added = 0

        for i in range(0, tam+1, 1):
            self.fila.append(NoFilaSequencial(None, None))

    def buscar(self, key):

        for i in range(1, self.tam_max+1, 1):
            if self.fila[i].key == key:
                return self.fila[i], key

        return None, None

    def inserir(self, key, value):
        # TODO procurar por keys nas outras filas

        if self.buscar(key)[1] is None:
            if self.last_added < self.tam_max:
                self.last_added += 1
                self.fila[self.last_added] = NoFilaSequencial(key, value)
            else:
                self.dobrar_transpor_fila()
                self.last_added += 1
                self.fila[self.last_added] = NoFilaSequencial(key, value)
        else:
            raise ChaveJaExiste

    def buscar_indice(self, key):
        for i in range(1, self.last_added+1, 1):
            if self.fila[i].key == key:
                return i

    def remover_por_key(self, key):

        if self.buscar(key)[1] is not None:
            indice = self.buscar_indice(key)
            removido = self.fila[indice]
            self.fila[indice] = NoFilaSequencial(None, None)

            for i in range(indice, self.last_added+1, 1):
                if i == self.last_added:
                    self.fila[i] = NoFilaSequencial(None, None)
                else:
                    self.fila[i] = self.fila[i+1]

            self.last_added -= 1
            return removido
        else:
            raise ChaveInexistente

    def remover(self):
        if self.last_added > 0:
            removido = self.fila[1]
            self.fila[1] = NoFilaSequencial(None, None)

            for i in range(1, self.last_added+1, 1):
                if i == self.last_added:
                    self.fila[i] = NoFilaSequencial(None, None)
                else:
                    self.fila[i] = self.fila[i+1]

            self.last_added -= 1
            return removido
        else:
            raise FilaUnderflow

    def dobrar_transpor_fila(self):
        nova_fila = []
        self.tam_max = self.tam_max*2

        for i in range(0, self.tam_max+1, 1):
            if i != 0 and i <= self.last_added:
                nova_fila.append(self.fila[i])
            else:
                nova_fila.append(NoFilaSequencial(None, None))

        self.fila = nova_fila

    def to_string(self):
        res = ''
        if self.last_added == 0:
            return res

        for i in range(1, self.last_added+1, 1):
            res = res + f' | {self.fila[i].value}'

        return res


class QuickSort:

    @classmethod
    def particionar(cls, array, p, r):

        x = array[r].value
        i = p - 1
        for j in range(p, r, 1):
            if array[j].value >= x:
                i = i + 1
                array[i], array[j] = array[j], array[i]

        array[i+1], array[r] = array[r], array[i+1]
        return i + 1

    @classmethod
    def quicksort(cls, array, p, r):
        if p < r:
            q = cls.particionar(array, p, r)
            cls.quicksort(array, p, q - 1)
            cls.quicksort(array, q + 1, r)
