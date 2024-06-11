import textwrap

def menu():
    menu = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova Conta
    [lc] Listas de Contas cadastradas
    [nu] Novo Usuario
    [q] Sair
    => """
    return input(textwrap.dedent(menu))

def deposito(saldo,valor,extrato,/):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        return saldo, extrato

    else:
        print("Operação falhou! O valor informado é inválido.")

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo

    excedeu_limite = valor > limite

    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
         print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        return saldo, extrato
    else:
        print("Operação falhou! O valor informado é inválido.")

def exibe_extrato(saldo, /,*, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))#Elimina caracteres especiais

    if len(cpf) != 11:# Verifica se o CPF tem 11 dígitos
        return False

    if cpf == cpf[0] * len(cpf): # Verifica se todos os dígitos são iguais (caso comum de CPFs inválidos)
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9)) # Calcula o primeiro dígito verificador
    primeiro_digito = (soma * 10 % 11) % 10
    if primeiro_digito != int(cpf[9]):
        return False

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10)) # Calcula o segundo dígito verificador
    segundo_digito = (soma * 10 % 11) % 10
    if segundo_digito != int(cpf[10]):
        return False

    return True

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]#verifica se a cpf igual/existente
    return usuarios_filtrados[0] if usuarios_filtrados else None

def cria_User(usuarios):
    cpf = input("Informe seu cpf: ")
    if validar_cpf(cpf) == False:
        print("CPF invalido")
        return
    else:
        print("CPF valido")

        usuario = filtrar_usuario(cpf, usuarios)

        if usuario:
            print("\n Já existe usuário com esse CPF!")
            return

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

        print("Usuário criado com sucesso!")

def nova_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    if validar_cpf(cpf) == False:
        print("CPF invalido")
        return
    else:
        print("CPF valido")
        usuario = filtrar_usuario(cpf, usuarios)

        if usuario:
            print("\nConta criada com sucesso!")
            return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

        print("\n Usuário não encontrado, fluxo de criação de conta encerrado! ")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    LIMITE_SAQUES = 3
    AGENCIA = "001"
    while True:

        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = deposito(saldo, valor, extrato )

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato = saque(saldo = saldo, valor = valor, extrato = extrato, limite = limite, numero_saques = numero_saques, limite_saques= LIMITE_SAQUES )
            

        elif opcao == "e":
            exibe_extrato(saldo, extrato=extrato)

        elif opcao == "nc":
            nu_conta = len(contas) + 1
            conta = nova_conta(AGENCIA, nu_conta, usuarios)

            if conta:
                contas.append(conta)
            

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "nu":
            cria_User(usuarios)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()