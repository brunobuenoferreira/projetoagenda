import sqlite3, random
from datetime import date
import os

def openConnectionDB():

    try:
        con = sqlite3.connect("bancoagenda")
        cur = con.cursor()

        return con, cur
    except:
        print("Conexão com o banco SQLITE falhou")

def menu():
    print(
    '''
    [ 1 ] - Consultar horários disponíveis
    [ 2 ] - Limpar Horário Cadastrado
    [ 3 ] - Verificar Horários e Quadras Locadas
    [ 4 ] - Consultar Valores a Pagar
    [ 5 ] - Limpar Toda a Agenda
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

def cadastroCliente(cpf):
    con, cur = openConnectionDB()
    listaCliente = []

    for row in cur.execute("SELECT * from cliente"):
        listaCliente.append(row[0])

    if cpf in listaCliente:
        print('Cliente já possui cadastro no sistema')
    else:
        print('Será necessário realizar o cadastro do cliente ...')
        nome = str(input('Nome do cliente: '))
        tel = str(input('Telefone: '))
        cur.execute('INSERT OR IGNORE INTO cliente (cpf, nome, tel) VALUES (?,?,?)', (cpf, nome, tel))
        print('Cliente cadastrado com sucesso!')

    con.commit()
    cur.close()
    con.close()

def consultaHorarios(data, opcao):
    con, cur = openConnectionDB()
    listaDATA = []

    if opcao == 1:
        for row in cur.execute('SELECT * FROM agenda'):
            listaDATA.append(row[1])

        if data in listaDATA:
            lista = []

            for q in range(1,5):
                lista = []
                print(f'=================== Horários Quadra {q} ===================')
                for row in cur.execute('SELECT * FROM agenda WHERE data = "{}" and quadra = {}'. format(data, q)):
                    lista.append(row[2])
            
                if len(lista) == 12:
                    msg = 'Não há mais horários disponíveis para essa data'
                    return msg

                for row in cur.execute('SELECT * FROM horarios'):
                    if row[0] in lista:
                        continue
                    else:
                        print(f'{row[0]} | {row[1]}')
        else:
            print("Sem agendamento para essa data ainda. Todos os horários disponíveis!")
    elif opcao == 3:
        pass
    else:
        print('Opção inválida')
    
    con.commit()
    cur.close()
    con.close()

def agendarHorario(hrs, data):
    con, cur = openConnectionDB()
    valor = 0

    print("Escolha a quadra por 1, 2, 3 ou 4 e o horário pelo seu número de identificação")

    opcaoQuadra = str(input("Para qual quadra deseja agendar um horário? (1 , 2 , 3 ou 4): "))
    opcaoHora = int(input("Horário que deseja agendar: "))
    cpf = str(input("Atribuir agendamento para qual CPF?: "))
    cadastroCliente(cpf)

    cur.execute("INSERT OR IGNORE INTO agenda (data, idHora, cpf, quadra, valor, pago, tipoHora) VALUES (?,?,?,?,?,?,?)", (data, opcaoHora, cpf, opcaoQuadra, 00.00, "Não", hrs))

    for row in cur.execute("SELECT * from agenda WHERE cpf = {}".format(cpf)):
        valor = row[5]

    if opcao == 1:
        valor = valor + 100.00
    else:
        valor = valor + 250.00

    cur.execute('UPDATE agenda SET valor = {} WHERE cpf = {}'.format(valor, cpf))
    for row in cur.execute('SELECT * FROM cliente WHERE cpf = {}'.format(cpf)):
        print("Valor atribuido ao cliente {} !".format(row[1]))


    con.commit()
    cur.close()
    con.close()


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
            data = str(input('Verificar disponibilidade em qual data? '))
            print(""" 
                [ 1 ] - 1 Hora
                [ 3 ] - 3 Horas  
                [ 0 ] - Voltar
            """)
            opcao = int(input("Escolha a opcão com o horário desejado: "))
            consultaHorarios(data, opcao)
        elif opcao == 2:
            print(""" 
            [ 1 ] - Agendar 1 Hora
            [ 3 ] - Agendar por 3 Horas  
            [ 0 ] - Voltar
            """)

            hrs = int(input('Por quantas horas? '))
            data = input('Agendar para qual data? ')
            agendarHorario(hrs, data)
        elif opcao == 3:
            cpf = input('CPF do cliente: ')
            cadastroCliente(cpf)