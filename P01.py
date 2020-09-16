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

        x = array[r].value.iniciativa
        i = p - 1
        for j in range(p, r, 1):
            if array[j].value.iniciativa >= x:
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


class Lutador:

    def __init__(self, key, time, dano, hp, iniciativa):
        self.key = key
        self.time = time
        self.dano = dano
        self.hp = hp
        self.iniciativa = iniciativa
        self.atacou = False
        self.vivo = True


class Time:

    def __init__(self, numero_id):
        self.numero_id = numero_id             # Identificador dos times controlado internamente pela programa.
        self.lutadores = FilaSequencial(10)    # Inicialmente tamanho 10, mas pode aumentar.
        self.cemiterio = FilaSequencial(10)
        self.score = 0

    def get_lutadores_size(self):
        return self.lutadores.last_added

    def get_cemiterio_size(self):
        return self.cemiterio.last_added

    def ordenar_lutadores(self):
        if self.lutadores.last_added == 1 or self.lutadores.last_added == 0:
            return

        QuickSort.quicksort(self.lutadores.fila, 1, self.lutadores.last_added)

    def ordenar_cemiterio(self):
        if self.cemiterio.last_added == 1 or self.cemiterio.last_added == 1:
            return

        QuickSort.quicksort(self.cemiterio.fila, 1, self.cemiterio.last_added)

    def lutadores_to_string(self):
        if self.lutadores.last_added == 0:
            return 'Fila de lutadores vazia'

        res = ''

        if self.lutadores.last_added == 1:
            res = res + f'Identificador do lutador: {self.lutadores.fila[1].value.key}\n'
            res = res + f'Iniciativa: {self.lutadores.fila[1].value.iniciativa}\n'
            res = res + f'Pontos de vida restantes: {self.lutadores.fila[1].value.hp}\n\n'

            return res

        for i in range(1, self.lutadores.last_added+1, 1):
            res = res + f'Posição na fila: {i}\n'
            res = res + f'Identificador do lutador: {self.lutadores.fila[i].value.key}\n'
            res = res + f'Iniciativa: {self.lutadores.fila[i].value.iniciativa}\n'
            res = res + f'Pontos de vida restantes: {self.lutadores.fila[i].value.hp}\n\n'

        return res

    def cemiterio_to_string(self):
        if self.cemiterio.last_added == 0:
            return 'Cemiterio vazio'

        res = ''

        if self.cemiterio.last_added == 1:
            res = res + f'Identificador do lutador: {self.cemiterio.fila[1].value.key}\n'
            res = res + f'Iniciativa: {self.cemiterio.fila[1].value.iniciativa}\n'
            res = res + f'Pontos de vida restantes: {self.cemiterio.fila[1].value.hp}\n\n'

            return res

        for i in range(1, self.cemiterio.last_added+1, 1):
            res = res + f'Posição na fila: {i}\n'
            res = res + f'Identificador do lutador: {self.cemiterio.fila[i].value.key}\n'
            res = res + f'Iniciativa: {self.cemiterio.fila[i].value.iniciativa}\n'
            res = res + f'Pontos de vida restantes: {self.cemiterio.fila[i].value.hp}\n\n'

        return res


class Game:
    time1 = Time(1)
    time2 = Time(2)

    @classmethod
    def turno(cls):
        time_id_input = 0
        lutador_key_input = 0
        dano_input = 0
        hp_input = 0
        iniciativa_input = 1
        time_id_input = 0
        decisao_input = 0

        # PRIMEIRA ETAPA
        # INSERÇÃO DE LUTADORES EM TIMES
        while True:
            print('Inserção de lutadores nos times.')
            print('Não são permitidas keys duplicadas.')
            print('')

            print('Digite qualquer tecla para continuar.')
            print('Digite 0 para ir para a próxima etapa.')
            decisao_input = input('Digite sua decisao: ')

            if int(decisao_input) == 0:
                break

            while True:
                time_id_input = input('Escolha o time que deseja adicionar um lutador. Digite 1 ou 2: ')
                if int(time_id_input) != 1 and int(time_id_input) != 2:
                    print('Digite apenas 1 ou 2!')
                    print('')
                else:
                    break

            while True:
                lutador_key_input = input('Digite a key, o número inteiro identificador do lutador: ')
                if isinstance(int(lutador_key_input), int):    # qq eu to fazendo
                    if cls.time1.lutadores.buscar(int(lutador_key_input))[1] is not None:
                        print('Esse identificador já é usado e está nos lutadores do time 1.')
                        print('')
                    elif cls.time1.cemiterio.buscar(int(lutador_key_input))[1] is not None:
                        print('Esse identificador já é usado e está no cemitério do time 1.')
                        print('')
                    elif cls.time2.lutadores.buscar(int(lutador_key_input))[1] is not None:
                        print('Esse identificador já é usado e está nos lutadores do time 2.')
                        print('')
                    elif cls.time2.cemiterio.buscar(int(lutador_key_input))[1] is not None:
                        print('Esse identificador já é usado e está no cemitério do time 2.')
                        print('')
                    else:
                        break
                else:
                    print('Digite apenas números inteiros')
                    print('')

            while True:
                dano_input = input('Digite o valor do dano: ')
                if int(dano_input) <= 0:
                    print('Não são permitidos valores menores ou iguais a 0.')
                    print('')
                else:
                    break

            while True:
                hp_input = input('Digite o número de pontos de vida do lutador: ')
                if int(hp_input) <= 0:
                    print('Não são permitidos valores menores ou iguais a 0.')
                    print('')
                else:
                    break

            while True:
                iniciativa_input = input('Digite um valor de 1 a 100 para o valor de iniciativa do lutador: ')
                if int(iniciativa_input) < 1 or int(iniciativa_input) > 100:
                    print('O valor deve ser entre 1 e 100.')
                else:
                    break

            lutador = Lutador(int(lutador_key_input), int(time_id_input), int(dano_input), int(hp_input), int(iniciativa_input))
            if int(time_id_input) == 1:
                cls.time1.lutadores.inserir(int(lutador_key_input), lutador)
            else:
                cls.time2.lutadores.inserir(int(lutador_key_input), lutador)

        print('\n\n\n')

        # RELATÓRIO DE STATUS DE UM TIME
        # Ordenação das filas em ordem decrescente
        cls.time1.ordenar_lutadores()
        cls.time1.ordenar_cemiterio()
        cls.time2.ordenar_lutadores()
        cls.time2.ordenar_cemiterio()
        while True:
            print('Relatório de times')
            print('Digite 1 para continuar ou qualquer outra tecla para ir para a próxima etapa.')
            decisao_input = input('Digite: ')
            if int(decisao_input) != 1:
                break

            while True:
                time_id_input = input('Digite o id do time, 1 ou 2, que você deseja ver o relatório: ')
                try:
                    if int(time_id_input) != 1 and int(time_id_input) != 2:
                        print('Digite apenas 1 ou 2!')
                        print('')
                    else:
                        break
                except ValueError as err:
                    print(err.__str__())
                    print('')

            try:
                if int(time_id_input) == 1:
                    print('Relatório do time 1: ')
                    print('Relatório de lutadores')
                    print(cls.time1.lutadores_to_string())
                    print('Relatório de cemitério')
                    print(cls.time1.cemiterio_to_string())
                    print('')
                else:
                    print('Relatório do time 2: ')
                    print('Relatório de lutadores')
                    print(cls.time2.lutadores_to_string())
                    print('Relatório de cemitério')
                    print(cls.time2.cemiterio_to_string())
            except ValueError as err:
                print(err.__str__())
                print('')


def main():
    Game.turno()

if __name__ == "__main__":
    main()