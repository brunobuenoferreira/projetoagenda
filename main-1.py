import sqlite3
from datetime import date
import os

def openConnectionDB():
    try:
        con = sqlite3.connect("agenda.db")
        cur = con.cursor()

        return con, cur
    except:
        print("Conexão com o banco SQLITE falhou")

def atribuirCPF(cpf, opcaoQuadra, opcaoHora, opcao):
    con, cur = openConnectionDB()
    listaCPF = []
    valor = 0

    for row in cur.execute("SELECT * from cliente WHERE cpf = {}".format(cpf)):
        valor = row[5]

    if opcao == 1:
        valor = valor + 100.00
    else:
        valor = valor + 250.00

    for row in cur.execute('SELECT cpf from cliente'):
        listaCPF.append(row[0])

    if cpf in listaCPF:
        cur.execute('UPDATE cliente SET idhora = {} WHERE cpf = {}'.format(opcaoHora, cpf))
        cur.execute('UPDATE cliente SET quadra = {} WHERE cpf = {}'.format(opcaoQuadra, cpf))
        cur.execute('UPDATE cliente SET valor = {} WHERE cpf = {}'.format(valor, cpf))
        for row in cur.execute('SELECT * from cliente WHERE cpf = {}'.format(cpf)):
            print("Valor atribuido ao cliente {} !".format(row[1]))
    else:
        nome = str(input("Nome do cliente: "))
        tel = str(input("Telefone do cliente: "))
        cur.execute("INSERT OR IGNORE INTO cliente (cpf, nome, telefone, quadra, idhora, valor) VALUES (?,?,?,?,?,?)", (cpf, nome, tel, opcaoQuadra, opcaoHora, valor))
        print("Usuário cadastrado com sucesso")

    con.commit()
    cur.close()
    con.close()

def agendarHorario():
    con, cur = openConnectionDB()

    print(""" 
    [ 1 ] - Agendar 1 Hora
    [ 3 ] - Agendar por 3 Hora  
    [ 0 ] - Voltar
    """)

    opcao = int(input("Escolha a opcão com o horário desejado: "))

    if opcao == 1:
        clear()
        verificarHorarios(1)
    elif opcao == 3:
        clear()
        verificarHorarios(3)
    else:
        clear()
        menu()

    print('')
    print("Escolha a quadra por 1, 2, 3 ou 4 e o horário pelo seu número de identificação")
    print('')
    opcaoQuadra = str(input("Qual QUADRA deseja agendar um horário? (1 , 2 , 3 ou 4): "))
    opcaoHora = int(input("Horário que deseja agendar: "))
    cpfCliente = str(input("Atribuir agendamento para qual CPF?: "))

    atribuirCPF(cpfCliente, opcaoQuadra, opcaoHora, opcao)

    # atualiza o valor para 1 no horario
    if opcao == 3:
        cur.execute('UPDATE quadra SET q{} = 1 WHERE id = {}'.format(opcaoQuadra, opcaoHora))
        cur.execute('UPDATE quadra SET q{} = 1 WHERE id = {}'.format(opcaoQuadra, opcaoHora+1))
        cur.execute('UPDATE quadra SET q{} = 1 WHERE id = {}'.format(opcaoQuadra, opcaoHora+2))
    else:
        cur.execute('UPDATE quadra SET q{} = 1 WHERE id = {}'.format(opcaoQuadra, opcaoHora))
    con.commit()

    cur.close()
    con.close()

def limparHorario():
    print("Esses são os horários das quadras locadas: ")

    print("Qual horário deseja desalugar? ")
    # VERIFICAR SE TEM 3 HORAS DE ANTECEDENCIA, SE NAO, DEVERA COBRAR

def verificarHorarios(n):
    hora = n
    con, cur = openConnectionDB()

    if hora == 1:
        print("Aqui está os horários disponíveis para a opção de 1 HORA: ")
        print("=================== Horários Quadra 1 ===================")
        for row in cur.execute('select * from quadra where q1 = "0"'):
            print(f'{row[0]} | {row[1]}')
        print("=================== Horários Quadra 2 ===================")
        for row in cur.execute('select * from quadra where q2 = "0"'):
            print(f'{row[0]} | {row[1]}')
        print("=================== Horários Quadra 3 ===================")
        for row in cur.execute('select * from quadra where q3 = "0"'):
            print(f'{row[0]} | {row[1]}')
        print("=================== Horários Quadra 4 ===================")
        for row in cur.execute('select * from quadra where q4 = "0"'):
            print(f'{row[0]} | {row[1]}')
    else:
        print("Aqui está os horários disponíveis para a opção de 3 HORAS: ")
        print("=================== Horários Quadra 1 ===================")
        horas = []
        ids = [] #armazena horarios vagos em uma lista, e sempre que o len da lista for 3, ele printa a index 0 e revove o mesmo da lista
        for row in cur.execute('select * from quadra'):
            if row[2] == 0:
                horas.append(row[1])
                ids.append(row[0])
            else:
                horas = []
                ids = []
            if len(horas) == 3:
                print(f'{ids[0]} | {horas[0]}')
                horas.remove(horas[0])
                ids.remove(ids[0])
                
        print("=================== Horários Quadra 2 ===================")
        horas = []
        ids = []
        for row in cur.execute('select * from quadra'):
            if row[3] == 0:
                horas.append(row[1])
                ids.append(row[0])
            else:
                horas = []
                ids = []
            if len(horas) == 3:
                print(f'{ids[0]} | {horas[0]}')
                horas.remove(horas[0])
                ids.remove(ids[0])
                

        print("=================== Horários Quadra 3 ===================")
        horas = []
        ids = []
        for row in cur.execute('select * from quadra'):
            if row[4] == 0:
                horas.append(row[1])
                ids.append(row[0])
            else:
                horas = []
                ids = []
            if len(horas) == 3:
                print(f'{ids[0]} | {horas[0]}')
                horas.remove(horas[0])
                ids.remove(ids[0])
                

        print("=================== Horários Quadra 4 ===================")
        horas = []
        ids = []
        for row in cur.execute('select * from quadra'):
            if row[5] == 0:
                horas.append(row[1])
                ids.append(row[0])
            else:
                horas = []
                ids = []
            if len(horas) == 3:
                print(f'{ids[0]} | {horas[0]}')
                horas.remove(horas[0])
                ids.remove(ids[0])
                

    cur.close()
    con.close()

def valoresPendentes():
    print("NAO SEI FAZER")

def exportarAgenda():
    print("NAO SEI FAZER")

def limparTodaAgenda():
    con, cur = openConnectionDB()

    print(""" 
    [ 1 ] - Sim! Limpar todos os horários da agenda
    [ 0 ] - Voltar ao menu
    """)

    opcao = int(input("Deseja limpar toda a agenda? : "))
    if opcao == 0:
        menu()
    else:
        try:
            cur.execute('UPDATE quadra SET q1 = 0 WHERE q1 = 1')
            cur.execute('UPDATE quadra SET q2 = 0 WHERE q2 = 1')
            cur.execute('UPDATE quadra SET q3 = 0 WHERE q3 = 1')
            cur.execute('UPDATE quadra SET q4 = 0 WHERE q4 = 1')
            con.commit()
            print("Agenda zerada!")
        except:
            print("Erro ao limpar agenda")
    cur.close()
    con.close()

def limparTodosOsClientes():
    con, cur = openConnectionDB()

    print(""" 
    [ 1 ] - Sim! Limpar todos os clientes cadastrados
    [ 0 ] - Voltar ao menu
    """)

    opcao = int(input("Deseja limpar toda a tabela cliente? : "))
    if opcao == 0:
        menu()
    else:
        try:
            cur.execute('DELETE from cliente')
            con.commit()
            print("Tabela de clientes zerada!")
        except:
            print("Erro ao limpar tabela")
    cur.close()
    con.close()

def menu():
    print(
    '''
    [ 1 ] - Agendar Novo Horario
    [ 2 ] - Limpar Horário Cadastrado
    [ 3 ] - Verificar Horários e Quadras Locadas
    [ 4 ] - Consultar Valores a Pagar
    [ 5 ] - Exportar Agendar Para CSV
    [ 6 ] - Limpar Toda a Agenda e Começar do Zero
    '''
    )

    opcao = int(input("Escolha uma opção: "))
    return opcao

def clear():
    import os

    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

if __name__ == "__main__":
    clear()
    opcao = 0

    print('''
    ================================
    ==== AGENDA DE BEACH TENNIS ====
    ================================
    ''')

    while opcao != 4:
        opcao = menu()
        if opcao == 1:
            agendarHorario()
        elif opcao == 2:
            limparHorario()
        elif opcao == 3:
            print(""" 
                [ 1 ] - Ver horários disponíveis para 1 Hora
                [ 3 ] - Ver horários disponíveis para 3 Horas
                """)
            opcao = int(input("Qual agenda gostaria de agendar? "))
            verificarHorarios(opcao)
        elif opcao == 4:
            valoresPendentes()
        elif opcao == 5:
            exportarAgenda()
        elif opcao == 6:
            limparTodaAgenda()
        elif opcao == 7:
            limparTodosOsClientes()
        else:
            clear()
            print("Opção inválida. Escolha outra opção.")