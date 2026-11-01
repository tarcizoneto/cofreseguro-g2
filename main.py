import os
from utils import csv
from datetime import datetime

CORES = {
    "RESET": "\033[0m",
    "ITALICO": "\033[3m",
    "NEGRITO": "\033[1m",
    "SUBLINHADO": "\033[4m",

    
    "VERMELHO": "\033[31m",
    "VERDE": "\033[32m",
    "AMARELO": "\033[33m",
    "AZUL": "\033[34m",
    "ROXO": "\033[35m",
    "CIANO": "\033[36m",
    "BRANCO": "\033[37m",
    "CINZA": "\033[90m",

    
    "BG_VERMELHO": "\033[41m",
    "BG_VERDE": "\033[42m",
    "BG_AZUL": "\033[44m"
}
DIRETORIOS = {
    'cofre': 'dados/cofre.csv',
    'senhasCom': 'dados/senhasComuns.csv',
    'log': 'dados/log.csv'
}


cofre = {}
senhasC = []
log = []

def printarLog(log, operacao=None):

    existemRegistros = False # essa variavel serve pra quando nao vai printar nenhum registro, é uma forma de verificação, quando chega depois do for, se a variavel continuar falsa, é porque não se printou registro nenhum
    if operacao is None:
        for registro in log:
            print(f"[{registro['quando']}] {registro['alteracoes']}")
            existemRegistros = True # pra dizer que se printou registros
        if not existemRegistros:
            print("O registro de auditoria está vazio.")
    else:
        for registro in log:
            if registro['operacao'] == operacao:
                print(f"[{registro['quando']}] {registro['alteracoes']}")
                existemRegistros = True
        if not existemRegistros:
            print("O registro de auditoria dessa categoria está vazio.")






def manipularSenha(acao, senha): # separei em função os atos de visualizar e criar, ja que em tempos futuros iremos fazer alguma criptografia
    match acao:
        case 'registrar':
            return senha # aqui vai ter o babado todo de criptografar
        case 'visualizar':
            return senha # e aqui vai ter o babado todo de descriptografar
        case 'previa':
            previaSenha = ''
            for idxLetra in range(len(senha)):
                if idxLetra <= 1:
                    previaSenha += senha[idxLetra]
                else:
                    previaSenha += '*'
            return previaSenha
                
        case _:
            raise ValueError(f'Mal uso da função de manipulação de senhas, {acao} não é uma ação válida')






def preparar(): 
    os.system("color && mode con cols=30 lines=30 && cls")

    # carregar arquivos necessários
    global cofre, senhasC, log
    
    cofre = csv.carregarCSV(DIRETORIOS["cofre"])
    senhasC = csv.carregarCSV(DIRETORIOS["senhasCom"])
    log = csv.carregarCSV(DIRETORIOS["log"], ehLista=True)

def main():
    preparar()
    global cofre, senhasC, log

    while True:
        os.system('cls')
        print(f"{CORES['VERDE']}=== CofreSeguro ==={CORES['RESET']}")

        print(f'\n\n{CORES["NEGRITO"]}Menus:{CORES["RESET"]} \n1. Senhas\n2. Categorias\n3. Registro de Auditoria\n0. Sair')
        menu = input("Digite o número do menu: ")
        os.system('cls')
        match menu:

            # menu de senhas
            case '1':
                while True:
                    os.system('cls')
                    print(f"{CORES['VERDE']}=== CofreSeguro ==={CORES['RESET']}")
                    print(f"{CORES['ITALICO']}Você está no menu de {CORES['NEGRITO']}senhas.{CORES['RESET']}")


                    print(f'\n\n{CORES["NEGRITO"]}Opções:{CORES["RESET"]} \n1. Adicionar senha\n2. Consultar senha\n3. Alterar senha\n4. Apagar senha\n5. Listar senhas\n6. Listar senhas por categoria\n0. Sair')
                    operacao = input('Digite o número da operação: ')
                    os.system('cls')
                    match operacao:
                        case '1':
                            print(f'{CORES["ITALICO"]}Você está adicionando uma senha, deixe o nome do serviço em branco para sair... {CORES["RESET"]}\n')
                            servico = input('Digite o nome de serviço no qual essa senha está sendo usada: ')
                            if servico == '':
                                continue
                            elif servico in cofre:
                                input(f"\n\nEsse serviço {CORES['NEGRITO']}já tem uma senha cadastrada!{CORES['RESET']}\nPressione alguma tecla para continuar...")
                                continue
                            cred = input("Digite a credencial (usuário, e-mail ou login) dessa senha: ")
                            senha = input("Digite a senha: ") # todo: alguma forma de criptografia
                            classe = input("Digite a categoria dessa credencial: ") # matheuzinho, saiba que depois a gente vai colocar pra ter como criar categorias e referencialas por indice e msotrar todas elas e tudo mais...
                            observacao = input(f"Digite uma observação para essa senha {CORES['ITALICO']}(ou deixe em branco, caso não queira){CORES['RESET']}: ")
                            horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            if observacao == '': # se nao tiver nada a ser observado
                                observacao = '-'
                            cofre[servico] = {
                                    'credencial': cred,
                                    'senha': manipularSenha('registrar', senha),
                                    'classe': classe,
                                    'registro': horario,
                                    'obs': observacao
                                }
                            
                            # registar no log
                            # salvar
                            csv.salvarCSV(DIRETORIOS["cofre"], cofre, 'servico')
                            log = csv.registrarLog(DIRETORIOS['log'], log, 'adicionar', servico)

                            input(f"\n\n{CORES['VERDE']}Senha do serviço {CORES['NEGRITO']}{servico}{CORES['RESET']} {CORES['VERDE']}adicionada com sucesso!{CORES['RESET']}\nPressione alguma tecla para continuar...")
                        case '2':
                            print(f'{CORES["ITALICO"]}Você está consultando uma senha, deixe o nome do serviço em branco para sair... {CORES["RESET"]}\n')
                            servico = input('Digite o nome do serviço da senha que você deseja consultar: ')
                            if servico == '':
                                continue

                            if servico in cofre:
                                log = csv.registrarLog(DIRETORIOS['log'], log, 'consultar', servico)
                                print(f"\n{CORES['VERDE']}A senha do serviço \"{servico}\" é {CORES['NEGRITO']}{manipularSenha('visualizar', cofre[servico]['senha'])}{CORES['RESET']}.")
                                
                            else:
                                print(f"\nEsse serviço {CORES['NEGRITO']}não está no cofre{CORES['RESET']}, verifique se você o digitou certo ou se ainda não adicionou-o.")

                            input('Pressione alguma tecla para continuar...')
                        case '3':
                            print(f'{CORES["ITALICO"]}Você está alterando uma senha, deixe o nome do serviço em branco para sair... {CORES["RESET"]}\n')
                            servico = input('Digite o nome do serviço da senha que você deseja alterar: ')
                            if servico == '':
                                continue

                            if servico in cofre:
                                
                                novaSenha = input("Digite a nova senha: ")

                                cofre[servico]['senha'] = manipularSenha('registrar', novaSenha)
                                cofre[servico]['horario'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                log = csv.registrarLog(DIRETORIOS['log'], log, 'alterar', servico)
                                print(f"\n{CORES['VERDE']}A senha do serviço \"{servico}\" foi {CORES['NEGRITO']}alterada!{CORES['RESET']}")

                                csv.salvarCSV(DIRETORIOS["cofre"], cofre, 'servico')
                            else:
                                print(f"\nEsse serviço {CORES['NEGRITO']}não está no cofre{CORES['RESET']}, verifique se você o digitou certo ou se ainda não adicionou-o.")

                            input('Pressione alguma tecla para continuar...')
                        case '4':
                            print(f'{CORES["ITALICO"]}Você está apagando uma senha, deixe o nome do serviço em branco para sair... {CORES["RESET"]}\n')
                            servico = input('Digite o nome do serviço da senha que você deseja apagar: ')
                            if servico == '':
                                continue

                            if servico in cofre:
                                
                                cofre.pop(servico)
                                log = csv.registrarLog(DIRETORIOS['log'], log, 'apagar', servico)
                                print(f"\n{CORES['VERDE']}A senha do serviço \"{servico}\" foi {CORES['NEGRITO']}apagada!{CORES['RESET']}")

                                csv.salvarCSV(DIRETORIOS["cofre"], cofre, 'servico')
                            else:
                                print(f"\nEsse serviço {CORES['NEGRITO']}não está no cofre{CORES['RESET']}, verifique se você o digitou certo ou se ainda não adicionou-o.")

                            input('Pressione alguma tecla para continuar...')
                        case '5':
                            if len(cofre) > 0:
                                print("Senhas salvas no CofreSeguro: ")
                                print(f"\n{CORES['NEGRITO']}{'Serviço':>16} {'Credencial':>24} {'Senha':>20} {'Categoria':>16} {'Observação':>64} {CORES['RESET']}")
                                for servico, dados in cofre.items():
                                    print(f"{servico:>16} {dados['credencial']:>24} {manipularSenha('previa', dados['senha']):>20} {dados['classe']:>16} {dados['obs']:>64}")
                            else:
                                print("Não há senhas no cofre!")
                            input('\nPressione alguma tecla para continuar...')
                        case '0':
                            break
                        case _:
                            input(f"Opção inválida!\nAperte qualquer tecla para tentar novamente...")
            case '2':
                while True:
                    os.system('cls')
                    print(f"{CORES['VERDE']}=== CofreSeguro ==={CORES['RESET']}")
                    print(f"{CORES['ITALICO']}Você está no menu de {CORES['NEGRITO']}categorias.{CORES['RESET']}")

                    
                    print(f'\n\n{CORES["NEGRITO"]}Opções:{CORES["RESET"]} \n1. Adicionar categoria\n2. Visualizar categorias\n3. Remover categoria\n0. Sair')
                    operacao = input('Digite o número da operação: ')
                    os.system('cls')
                    match operacao:
                        case '0':
                            break
                        case _:
                            input(f"Opção inválida!\nAperte qualquer tecla para tentar novamente...")
            case '3':
                while True:
                    os.system('cls')
                    print(f"{CORES['VERDE']}=== CofreSeguro ==={CORES['RESET']}")
                    print(f"{CORES['ITALICO']}Você está no menu de {CORES['NEGRITO']}registro de auditoria.{CORES['RESET']}")


                    print(f'\n\n{CORES["NEGRITO"]}Opções:{CORES["RESET"]} \n1. Visualizar registro completo\n2. Visualizar registro por operação\n0. Sair')
                    operacao = input('Digite o número da operação: ')
                    os.system('cls')
                    match operacao:
                        case '1':
                            print(f'Todos os registros: {CORES["CINZA"]}')
                            printarLog(log)
                            input(f'{CORES["RESET"]}\nPressione alguma tecla para continuar...')
                        case '2':
                            operacaoLog = input("Digite a operação para pesquisar nos registros (adicionar/consultar/alterar/apagar): ")
                            print(f'Registros da operação {operacaoLog}: {CORES["CINZA"]}')
                            printarLog(log, operacaoLog)
                            input(f'{CORES["RESET"]}\nPressione alguma tecla para continuar...')
                        case '0':
                            break
                        case _:
                            input(f"Opção inválida!\nAperte qualquer tecla para tentar novamente...")
            case '0':
                print("Fechando cofre...")
                break
            case _:
                input(f"Opção inválida!\nAperte qualquer tecla para tentar novamente...")
                


if __name__ == "__main__":
    # iniciar o programa
    main()
    
    
