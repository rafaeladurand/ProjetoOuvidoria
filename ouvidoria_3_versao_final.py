import mysql.connector

"""create table ouvidorias (
codigo int auto_increment, 
titulo varchar(200),
tipo varchar(200),
descricao varchar(500),
primary key(codigo)
)"""

class Ocorrencia:
    def __init__(self, titulo, tipo, descricao):
        self.titulo = titulo
        self.tipo = tipo
        self.descricao = descricao

class BancoDados:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345',
            database='ouvidoria')
    def inserir(self, ocorrencia):

        try:
            sql = f"""INSERT INTO ouvidorias (titulo,tipo,descricao) 
                                                                values('{ocorrencia.titulo}','{ocorrencia.tipo}', '{ocorrencia.descricao}')"""
            cursor = self.conexao.cursor()
            cursor.execute(sql)
            self.conexao.commit()

        except Exception:
            print('Inválido!')

    def listarTodosDados(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM ouvidorias")
        results = cursor.fetchall()
        return self.conversor_tupla_lista(results)

    def listarTodosCodigos(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT codigo FROM ouvidorias")
        results = cursor.fetchall()
        lista_codigos=[]
        for i in range(len(self.listarTodosDados())):
            lista_codigos.append(self.listarTodosDados()[i][0])

        return lista_codigos

    def listarPorCodigo(self, codigo):
        cursor = self.conexao.cursor()
        cursor.execute(f"SELECT * FROM ouvidorias WHERE codigo = {codigo}")
        ocorrencia_selecionada= self.conversor_tupla_lista(cursor.fetchall())[0]
        objeto_ocorrencia = Ocorrencia(ocorrencia_selecionada[1],ocorrencia_selecionada[2],ocorrencia_selecionada[3])


        return objeto_ocorrencia
    def removerPor(self,codigo):
        codigo_removido = self.listarPorCodigo(codigo)

        sql1 = f"DELETE FROM ouvidorias WHERE codigo = {codigo}"
        cursor = self.conexao.cursor()
        cursor.execute(sql1)
        self.conexao.commit()
        self.conexao.rollback()
        return codigo_removido

    def conversor_tupla_lista(self, lista):
        lista_convertida=[]
        for i in range(len(lista)):
            lista_convertida.append(list(lista[i]))
        return lista_convertida

class Ouvidoria:

    def __init__(self):
        self.bancodados = BancoDados()

    def menu(self):

        opcao = 0
        menu = '-' * 20

        while opcao != 5:
            print()
            print("{}BEM VINDO AO MENU{}".format(menu, menu))
            print()
            print("1) Listar as ocorrências")
            print("2) Adicionar nova ocorrência")
            print("3) Remover uma ocorrência")
            print("4) Pesquisar uma ocorrência por código")
            print("5) Sair do programa")
            print()

            opcao = int(input("Digite o número da sua opção: "))

            if opcao == 1:
                self.listar_ocorrencias()

            elif opcao == 2:
                self.adicionar_ocorrencia()

            elif opcao == 3:
                self.remover_ocorrencia()

            elif opcao == 4:
                self.pesquisar_ocorrencia()

            elif opcao == 5:
                print()
                print("Obrigado por utilizar nosso programa! Volte sempre.")

            else:
                print()
                print("Opção inválida!")


    def listar_ocorrencias(self):
        ocorrencias=self.bancodados.listarTodosDados()
        if not ocorrencias:
            print()
            print("Nenhuma ocorrência foi cadastrada no sistema!")
        else:
            categoria = input('''\n1) Elogio\n2) Reclamação\n3) Sugestão\n4) Todas\n \nDigite o número do tipo de ocorrência que deseja exibir: ''')
            if not categoria.isnumeric():
                return print(f'Opção inválida!')
            else:
                categoria = int(categoria)

                if categoria == 1:
                    categoria = 'Elogio'
                elif categoria == 2:
                    categoria = 'Reclamação'
                elif categoria == 3:
                    categoria = 'Sugestão'
                elif categoria == 4:
                    categoria = 'Todos'
                else:
                    return print(f'Código inválido!')
                codigo = [ocorrencia for ocorrencia in ocorrencias
                                     if categoria.title() == 'Todos' or str(ocorrencia[2]).lower() == categoria.title().lower()]
                if not codigo:
                    print()
                    print(f'Não há nenhuma ocorrência do tipo "{categoria}"!')
                else:
                    print()
                    for cont, itens in enumerate(codigo):
                        print(f'{itens[0]}) {itens[1]}')

    def adicionar_ocorrencia(self):
        print()
        print('Criando uma nova ocorrência...')
        print()
        tipo = input('''1) Elogio\n2) Reclamação\n3) Sugestão\n \nSelecione o número do tipo da ocorrência: ''')
        if not tipo.isnumeric():
            return print('Opção inválida!')
        else:
            tipo = int(tipo)

            if tipo == 1:
                tipo = 'Elogio'
            elif tipo == 2:
                tipo = 'Reclamação'
            elif tipo == 3:
                tipo = 'Sugestão'
            else:
                return print(f'Código inválido!')

        titulo = str(input('Digite o título da ocorrência: ')).capitalize()
        descricao = str(input("Digite a descrição da sua ocorrência: ")).capitalize()
        self.bancodados.inserir(Ocorrencia(titulo, tipo, descricao))
        print()
        print(f'Ocorrência cadastrada com sucesso! Código: {self.bancodados.listarTodosDados()[-1][0]}')
    def remover_ocorrencia(self):
        ocorrencias = self.bancodados
        if not ocorrencias.listarTodosDados():
            print()
            print("Nenhuma ocorrência cadastrada no sistema!")
        else:
            print()
            codigo = int(input("Digite o código da ocorrência que deseja remover: "))
            if (not codigo in ocorrencias.listarTodosCodigos()):
              print("Código inválido!")
            else:
                ocorrencia_removida = ocorrencias.removerPor(codigo)
                print()
                print(f"A ocorrência foi removida com sucesso!")

    def pesquisar_ocorrencia(self):
        ocorrencias = self.bancodados
        if not ocorrencias.listarTodosDados():
            print()
            print("Nenhuma ocorrência cadastrada no sistema!")
            print()
        else:
            print()
            codigo = int(input("Digite o código da ocorrência que deseja pesquisar: "))
            if( not codigo in ocorrencias.listarTodosCodigos()):
                print("Código inválido!")
            else:
                ocorrencia = ocorrencias.listarPorCodigo(codigo)
                print()
                print("\nTítulo: ", ocorrencia.titulo)
                print("Tipo: ", ocorrencia.tipo)
                print("Descrição: ", ocorrencia.descricao)

ouvidoria = Ouvidoria()
ouvidoria.menu()

