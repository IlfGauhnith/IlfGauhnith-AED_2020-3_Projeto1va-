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

    def checar_saude(self):
        if self.hp <= 0:
            self.vivo = False
        else:
            self.vivo = True

        return self.vivo

    def __str__(self):
        res = f'Identificador do lutador: {self.key}\n'
        res = res + f'Time: {self.time}\n'
        res = res + f'HP: {self.hp}\n'
        res = res + f'Dano: {self.dano}\n'
        res = res + f'Iniciativa: {self.iniciativa}\n'
        res = res + f'Atacou: {self.atacou}\n'
        res = res + f'Vivo: {self.vivo}\n'

        return res


class Time:

    def __init__(self, numero_id):
        self.numero_id = numero_id             # Identificador dos times controlado internamente pela programa.
        self.lutadores = FilaSequencial(10)    # Inicialmente tamanho 10, mas pode aumentar.
        self.cemiterio = FilaSequencial(10)
        self.score = 0

    def reiniciar_ataque(self):
        for i in range(1, self.get_lutadores_size()+1, 1):
            self.lutadores.fila[i].value.atacou = False

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
    def calcular_resultado(cls):
        # Retornar um valor inteiro representando o vencedor
        # 0 = Ainda não foi decidido, continuar jogo.
        # 1 = time1.
        # 2 = time2.
        # 3 = empate.

        cls.time1.score = cls.time2.get_cemiterio_size()
        cls.time2.score = cls.time1.get_cemiterio_size()

        if cls.time1.get_lutadores_size() == 0 and cls.time2.get_lutadores_size() == 0:
            return 3
        elif cls.time1.get_lutadores_size() == 0 and cls.time2.get_lutadores_size() >= 1:
            return 2
        elif cls.time2.get_lutadores_size() == 0 and cls.time1.get_lutadores_size() >= 1:
            return 1

        if cls.time1.get_lutadores_size() > 0 and cls.time2.get_lutadores_size() > 0:
            if cls.time1.score >= 20 and cls.time2.score < 20:
                return 1
            elif cls.time2.score >= 20 and cls.time1.score < 20:
                return 2
            elif cls.time1.score >= 20 and cls.time2.score >= 20:
                if cls.time1.score > cls.time2.score:
                    return 1
                elif cls.time2.score > cls.time1.score:
                    return 2
                else:
                    return 3
        elif cls.time1.get_lutadores_size() == 0 and cls.time2.get_lutadores_size() == 0:
            return 3

        return 0

    @classmethod
    def play(cls):
        time_id_input = 0
        lutador_key_input = 0
        dano_input = 0
        hp_input = 0
        iniciativa_input = 1
        time_id_input = 0
        decisao_input = 0

        while True:
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

            print('')

            # FUGA DE UM LUTADOR
            while True:
                print('Fuga de lutadores!')
                print('Nesta etapa você pode escolher lutadores para fugir do combate!')
                print('Ele será removido permanentemente do jogo!')
                print('O lutador deve estar vivo e deve pertencer a um dos times.')

                print('')

                print('Digite 1 para continuar ou qualquer outra tecla para ir para a próxima etapa.')
                decisao_input = input('Digite: ')
                if int(decisao_input) != 1:
                    break

                while True:
                    lutador_key_input = input('Digite o identificador do lutador a ser removido: ')
                    try:
                        if cls.time1.lutadores.buscar(int(lutador_key_input))[1] is not None:
                            key = cls.time1.lutadores.buscar(int(lutador_key_input))[1]
                            lutador = cls.time1.lutadores.remover_por_key(key)
                            print('')
                            print(f'Lutador de identificador {key} fugiu do combate!')
                            print('')
                            del lutador
                            break
                        elif cls.time2.lutadores.buscar(int(lutador_key_input))[1] is not None:
                            key = cls.time2.lutadores.buscar(int(lutador_key_input))[1]
                            lutador = cls.time2.lutadores.remover_por_key(key)
                            print('')
                            print(f'Lutador de identificador {key} fugiu do combate!')
                            print('')
                            del lutador
                            break
                        else:
                            print('Identificador não existe em nenhum dos times!')
                    except ValueError as err:
                        print(err.__str__())
                        print('')

            # SEGUNDA ETAPA
            # COMBATE
            while True:
                if cls.time1.get_lutadores_size() == 0 or cls.time2.get_lutadores_size() == 0:
                    break

                no_fila_combatente1 = cls.time1.lutadores.remover()
                no_fila_combatente2 = cls.time2.lutadores.remover()

                print('')
                print(no_fila_combatente1.value.__str__())
                print(no_fila_combatente2.value.__str__())
                print('')

                # 1 e 2 não atacaram
                if not no_fila_combatente1.value.atacou and not no_fila_combatente2.value.atacou:
                    no_fila_combatente1.value.hp = no_fila_combatente1.value.hp - no_fila_combatente2.value.dano
                    no_fila_combatente2.value.hp = no_fila_combatente2.value.hp - no_fila_combatente1.value.dano
                    no_fila_combatente1.value.atacou = True
                    no_fila_combatente2.value.atacou = True

                    if no_fila_combatente1.value.checar_saude():
                        cls.time1.lutadores.inserir(no_fila_combatente1.key, no_fila_combatente1.value)
                    else:
                        cls.time1.cemiterio.inserir(no_fila_combatente1.key, no_fila_combatente1.value)

                    if no_fila_combatente2.value.checar_saude():
                        cls.time2.lutadores.inserir(no_fila_combatente2.key, no_fila_combatente2.value)
                    else:
                        cls.time2.cemiterio.inserir(no_fila_combatente2.key, no_fila_combatente2.value)

                # 1 não atacou e 2 atacou
                elif not no_fila_combatente1.value.atacou and no_fila_combatente2.value.atacou:
                    no_fila_combatente2.value.hp = no_fila_combatente2.value.hp - no_fila_combatente1.value.dano
                    no_fila_combatente1.value.atacou = True

                    if no_fila_combatente1.value.checar_saude():
                        cls.time1.lutadores.inserir(no_fila_combatente1.key, no_fila_combatente1.value)
                    else:
                        cls.time1.cemiterio.inserir(no_fila_combatente1.key, no_fila_combatente1.value)

                    if no_fila_combatente2.value.checar_saude():
                        cls.time2.lutadores.inserir(no_fila_combatente2.key, no_fila_combatente2.value)
                    else:
                        cls.time2.cemiterio.inserir(no_fila_combatente2.key, no_fila_combatente2.value)

                # 1 atacou e 2 não atacou
                elif no_fila_combatente1.value.atacou and not no_fila_combatente2.value.atacou:
                    no_fila_combatente1.value.hp = no_fila_combatente1.value.hp - no_fila_combatente2.value.dano
                    no_fila_combatente2.value.atacou = True

                    if no_fila_combatente1.value.checar_saude():
                        cls.time1.lutadores.inserir(no_fila_combatente1.key, no_fila_combatente1.value)
                    else:
                        cls.time1.cemiterio.inserir(no_fila_combatente1.key, no_fila_combatente1.value)

                    if no_fila_combatente2.value.checar_saude():
                        cls.time2.lutadores.inserir(no_fila_combatente2.key, no_fila_combatente2.value)
                    else:
                        cls.time2.cemiterio.inserir(no_fila_combatente2.key, no_fila_combatente2.value)

                elif no_fila_combatente1.value.atacou and no_fila_combatente2.value.atacou:
                    cls.time1.lutadores.inserir(no_fila_combatente1.key, no_fila_combatente1.value)
                    cls.time2.lutadores.inserir(no_fila_combatente2.key, no_fila_combatente2.value)
                    cls.time1.reiniciar_ataque()
                    cls.time2.reiniciar_ataque()
                    break


            print('FASE DE RESULTADOS!')
            if cls.calcular_resultado() == 1:
                print('TIME 1 VENCEU!')
                break
            elif cls.calcular_resultado() == 2:
                print('TIME 2 VENCEU!')
                break
            elif cls.calcular_resultado() == 3:
                print('EMPATE!')
                break
            print('O jogo continua...')



def main():
    Game.play()


if __name__ == "__main__":
    main()