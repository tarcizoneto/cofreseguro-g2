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
    'log': 'dados/log.csv',
    'categorias': 'dados/categorias.csv'
}


cofre = {}
senhasC = []
log = []
categorias = []

def limparTerminal(): # a merda do windows quer ser diferentão e usar "cls" pra limpar o terminal, mas o resto usa o comando clear (linux,mac), criei essa bomba de função
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

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


def printarCategorias(categorias, mostrarIndices = True): # mostrarIndices indica se o programa quer que mostre os índices ou não, no caso de remover categoria, onde o usuario digita o nome inteiro
                                                          # não precisa mostrar os indices (1. Jogos), esse numeroiznhho aí
    if len(categorias) != 0:
        for i in range(len(categorias)):
            if mostrarIndices:
                print(f"{i+1}. {categorias[i]}")
            else:
                print(f"{categorias[i]}")
    else:
        print(f'{CORES["VERMELHO"]}Não há categorias registradas!{CORES["RESET"]}')

def printarCofre(cofre, categoriaAnalisar=None): # criamos essa função pra printar as senhas de um dicionario desejado, já que além da listagem normal, tem a listagem entre categorias, ficaria uma bagunça isso jogado duas vezes no código 

    printouSenhas = False # essa variável serve pra verificar se a função printou alguma senha ou não, já que não tem como verificar se existe alguma senha

    if len(cofre) > 0:
        print(f"\n{CORES['NEGRITO']}{'Serviço':>16} {'Credencial':>24} {'Senha':>20} {'Categoria':>16} {'Observação':>40} {CORES['RESET']}") # cabeçalho

        if categoriaAnalisar is not None: # se, na hora que chamarem a função, o programa der a categoria a analisar, como acontece no listar senha por categorias,
                                          # a função entende que tem que caçar as senhas e printar só as que forem da categoria pedida
            for servico, dados in cofre.items():
                if categorias[categoriaAnalisar] == dados['categoria']: # to percorrendo todas as senhas, se esta estiver com a caegoria que eu pedi, entao printa!
                    printouSenhas = True # no momento em que printar uma senha, a variavel se torna true e lá no final, não precisa mais printar que não existe nenhuma senha
                    print(f"{servico:>16} {dados['credencial']:>24} {manipularSenha('previa', dados['senha']):>20} {dados['categoria']:>16} {dados['obs']:>40}")
            if not printouSenhas: # se nao printou nenhuma senha, é porque não tem nenhuma senha com essa categoria.
                print(f"{CORES['VERMELHO']}Não há senhas salvas com essa categoria.{CORES['VERMELHO']}")
        else: # se não, printa logo tudo mesmo
            for servico, dados in cofre.items():
                print(f"{servico:>16} {dados['credencial']:>24} {manipularSenha('previa', dados['senha']):>20} {dados['categoria']:>16} {dados['obs']:>40}")
    else:
        print(f"{CORES['VERMELHO']}Não há senhas no cofre!{CORES['RESET']}")


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


# essa função serviria caso a gente não tivesse um csv para salvar as categorias, e daí precisaríamos buscar as categorias ao percorrer todas as senhas,
# mas agora, nós salvamos as categorias em csv.
# def acharCategorias(cofre):
#     categorias = []
#     for servico in cofre.values():
#         if servico['categoria'] not in categorias:
#             if 'categoria' in servico:
#                 categorias.append(servico['categoria'])
#     return categorias



def preparar(): 
    os.system("color && mode con cols=30 lines=30")
    limparTerminal()

    # carregar arquivos necessários
    global cofre, senhasC, log, categorias
    
    cofre = csv.carregarCSV(DIRETORIOS["cofre"])
    senhasC = csv.carregarCSV(DIRETORIOS["senhasCom"])
    log = csv.carregarCSV(DIRETORIOS["log"], ehLista=True)
    categorias = csv.carregarCSV(DIRETORIOS["categorias"])

def main():
    preparar()
    global cofre, senhasC, log, categorias

    while True:
        limparTerminal()
        print(f"{CORES['VERDE']}=== CofreSeguro ==={CORES['RESET']}")

        print(f'\n\n{CORES["NEGRITO"]}Menus:{CORES["RESET"]} \n1. Senhas\n2. Categorias\n3. Registro de Auditoria\n0. Sair')
        menu = input("Digite o número do menu: ")
        limparTerminal()
        match menu:

            # menu de senhas
            case '1':
                while True:
                    limparTerminal()
                    print(f"{CORES['VERDE']}=== CofreSeguro ==={CORES['RESET']}")
                    print(f"{CORES['ITALICO']}Você está no menu de {CORES['NEGRITO']}senhas.{CORES['RESET']}")


                    print(f'\n{CORES["NEGRITO"]}Opções:{CORES["RESET"]} \n1. Adicionar senha\n2. Consultar senha\n3. Alterar senha\n4. Apagar senha\n5. Listar senhas\n6. Listar senhas por categoria\n7. Apagar todas as senhas {CORES["VERMELHO"]}{CORES["NEGRITO"]}(USE COM CUIDADO){CORES["RESET"]}\n0. Sair')
                    operacao = input('Digite o número da operação: ')
                    limparTerminal()
                    match operacao:
                        case '1':
                            print(f'{CORES["ITALICO"]}Você está adicionando uma senha, deixe o nome do serviço em branco para sair... {CORES["RESET"]}\n') # uma ótima funcionalidade é pra que, caso o usuario queira sair e não quer realmente adicionar uma senha, só precisa deixar em branco 
                            servico = input('Digite o nome de serviço no qual essa senha está sendo usada: ').capitalize()
                            if servico == '': # o programa vê se ta em branco, e se tiver, é porque o usuario quer sair
                                continue # entao a gente sai
                            elif servico in cofre:
                                input(f"\n\nEsse serviço {CORES['NEGRITO']}já tem uma senha cadastrada!{CORES['RESET']}\nPressione Enter para continuar...")
                                continue
                            cred = input("Digite a credencial (usuário, e-mail ou login) dessa senha: ")
                            senha = input("Digite a senha: ") # todo: alguma forma de criptografia
                            if len(categorias) > 0: # só se pode escolher uma categoria pra senha se existirem categorias, se nao tiver nenhuma por enquanto
                                print(f"\nCategorias disponíveis:{CORES['CINZA']}")
                                printarCategorias(categorias)
                                while True: # loop basiquinho pra forçar o usuário a digitar uma categoria válida, se o número não estiver no alcance, ele repete até estar
                                    categoria = int(input(f"{CORES['RESET']}Digite a categoria desejada com base na lista acima (de 1 a {len(categorias)}): ")) - 1
                                    if categoria < 0 or categoria > (len(categorias) - 1):
                                        print(f'{CORES["VERMELHO"]}Categoria inválida, digite um número de 1 a {len(categorias)}.{CORES["RESET"]}') # olha aí, digite um numero de 1 até 4, por exemplo, se tiver 4 categorias
                                    else:
                                        break
                                categoriaEscolhida = categorias[categoria]
                            else:
                                categoriaEscolhida = '-'
                                print(f"{CORES['CINZA']}{CORES['ITALICO']}Não existe nenhuma categoria, altere a senha em outro momento para assignar esse serviço a uma.{CORES['RESET']}")
                            observacao = input(f"Digite uma observação para essa senha {CORES['ITALICO']}(ou deixe em branco, caso não queira){CORES['RESET']}: ")
                            horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            if observacao == '': # se nao tiver nada a ser observado
                                observacao = '-'
                            cofre[servico] = {
                                    'credencial': cred,
                                    'senha': manipularSenha('registrar', senha),
                                    'categoria': categoriaEscolhida,
                                    'registro': horario,
                                    'obs': observacao
                                }
                            
                            # registar no log
                            # salvar
                            csv.salvarCSV(DIRETORIOS["cofre"], cofre, 'servico')
                            log = csv.registrarLog(DIRETORIOS['log'], log, 'adicionar', servico)

                            input(f"\n\n{CORES['VERDE']}Senha do serviço {CORES['NEGRITO']}{servico}{CORES['RESET']} {CORES['VERDE']}adicionada com sucesso!{CORES['RESET']}\nPressione Enter para continuar...")
                        case '2':
                            print(f'{CORES["ITALICO"]}Você está consultando uma senha, deixe o nome do serviço em branco para sair... {CORES["RESET"]}\n')
                            servico = input('Digite o nome do serviço da senha que você deseja consultar: ').capitalize()
                            if servico == '':
                                continue

                            if servico in cofre:
                                log = csv.registrarLog(DIRETORIOS['log'], log, 'consultar', servico)
                                print(f"\n{CORES['VERDE']}A credencial do serviço \"{servico}\" é {CORES['NEGRITO']}{cofre[servico]['credencial']}{CORES['RESET']}{CORES['VERDE']}, e sua senha é {CORES['NEGRITO']}{manipularSenha('visualizar', cofre[servico]['senha'])}{CORES['RESET']}.")
                                
                            else:
                                print(f"\nEsse serviço {CORES['NEGRITO']}não está no cofre{CORES['RESET']}, verifique se você o digitou certo ou se ainda não adicionou-o.")

                            input('Pressione Enter para continuar...')
                        case '3':
                            print(f'{CORES["ITALICO"]}Você está alterando uma senha, deixe o nome do serviço em branco para sair... {CORES["RESET"]}\n')
                            servico = input('Digite o nome do serviço da senha que você deseja alterar: ').capitalize()
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

                            input('Pressione Enter para continuar...')
                        case '4':
                            print(f'{CORES["ITALICO"]}Você está apagando uma senha, deixe o nome do serviço em branco para sair... {CORES["RESET"]}\n')
                            servico = input('Digite o nome do serviço da senha que você deseja apagar: ').capitalize()
                            if servico == '':
                                continue

                            if servico in cofre:
                                
                                cofre.pop(servico)
                                log = csv.registrarLog(DIRETORIOS['log'], log, 'apagar', servico)
                                print(f"\n{CORES['VERDE']}A senha do serviço \"{servico}\" foi {CORES['NEGRITO']}apagada!{CORES['RESET']}")

                                csv.salvarCSV(DIRETORIOS["cofre"], cofre, 'servico')
                            else:
                                print(f"\nEsse serviço {CORES['NEGRITO']}não está no cofre{CORES['RESET']}, verifique se você o digitou certo ou se ainda não adicionou-o.")

                            input('Pressione Enter para continuar...')
                        case '5':
                            print("Senhas salvas no CofreSeguro: ")
                            printarCofre(cofre)
                            input('\nPressione Enter para continuar...')
                        case '6':
                            if len(categorias) > 0: # pra poder listar as senhas por categorias, se precisa de uma categoria, se a lista de categorias tiver vazia, entao fudeu
                                print(f"\nCategorias disponíveis:{CORES['CINZA']}")
                                printarCategorias(categorias)
                                while True:
                                    categoriaAnalisada = int(input(f"{CORES['RESET']}Digite a categoria desejada com base na lista acima (de 1 a {len(categorias)}): ")) - 1
                                    if categoriaAnalisada < 0 or categoriaAnalisada > (len(categorias) - 1):
                                        print(f"{CORES['VERMELHO']}Categoria inválida, digite um número de 1 a {len(categorias)}.{CORES['RESET']}")
                                    else:
                                        break
                                limparTerminal()
                                print(f"Senhas salvas com a categoria {CORES['NEGRITO']}{categorias[categoriaAnalisada]}{CORES['RESET']}: \n")
                                printarCofre(cofre, categoriaAnalisada)
                            else: # fudeu
                                print(f"{CORES['VERMELHO']}Para se listar senhas por categoria, é preciso que exista {CORES['NEGRITO']}pelo menos uma categoria.")
                            input(f"{CORES['RESET']}\nPressione Enter para continuar...")
                        case '7':
                            apagar = input(f'{CORES["VERMELHO"]}Você escolheu apagar todas as senhas, escreva {CORES["NEGRITO"]}\"SIM\"{CORES["RESET"]}{CORES["VERMELHO"]} para confirmar ou pressione Enter para sair:{CORES["RESET"]} ').upper()
                            if apagar == "SIM":
                                cofre = {}
                                print(f"As senhas foram apagadas")
                                log = csv.registrarLog(DIRETORIOS['log'], log, 'apagar', "Todas as senhas")
                                csv.salvarCSV(DIRETORIOS["cofre"], cofre, 'servico')
                                
                                input(f"{CORES['RESET']}\nPressione Enter para continuar...")
                            else:
                                continue
                        case '0':
                            break
                        case _:
                            input(f"Opção inválida!\nPressione Enter para tentar novamente...")
            case '2':
                while True:
                    limparTerminal()
                    print(f"{CORES['VERDE']}=== CofreSeguro ==={CORES['RESET']}")
                    print(f"{CORES['ITALICO']}Você está no menu de {CORES['NEGRITO']}categorias.{CORES['RESET']}")

                    
                    print(f'\n\n{CORES["NEGRITO"]}Opções:{CORES["RESET"]} \n1. Adicionar categoria\n2. Visualizar categorias\n3. Remover categoria\n0. Sair')
                    operacao = input('Digite o número da operação: ')
                    limparTerminal()
                    match operacao:
                        case '1':
                            print(f'{CORES["ITALICO"]}Você está removendo uma categoria, deixe o nome da categoria em branco para sair... {CORES["RESET"]}\n')

                            novaCategoria = input("\nDigite a categoria a ser adicionada: ").capitalize()
                            if novaCategoria == '':
                                continue

                            if novaCategoria not in categorias: # se já nao existir uma categoria, entao eh p adicionar essa
                                categorias.append(novaCategoria)
                                csv.salvarCSV(DIRETORIOS["categorias"], categorias, 'categoria')
                                print(f"\n\n{CORES['VERDE']}A categoria {CORES['NEGRITO']}{novaCategoria}{CORES['RESET']} {CORES['VERDE']}foi adicionada!")
                            else: # e avisar se já existe a catgoria
                                print(f'{CORES["VERMELHO"]}A categoria {CORES["NEGRITO"]}{novaCategoria}{CORES["RESET"]} {CORES["VERMELHO"]}já se encontra na lista de categorias!{CORES["RESET"]}')
                            input(f"{CORES['RESET']}\nPressione Enter para continuar...")
                        case '2':
                            print(f"As categorias atuais são:{CORES['CINZA']}")
                            printarCategorias(categorias)
                            input(f"{CORES['RESET']}\nPressione Enter para continuar...")
                        case '3':
                            print(f'{CORES["ITALICO"]}Você está removendo uma categoria, deixe o nome da categoria em branco para sair... {CORES["RESET"]}\n')
                            
                            print(f"\nAs categorias atuais são:{CORES['CINZA']}")
                            printarCategorias(categorias, mostrarIndices=False)
                            removCategoria = input(f"{CORES['RESET']}Digite a categoria a ser removida: ").capitalize()
                            if removCategoria == '':
                                continue

                            if removCategoria in categorias: # só remover se existir, né
                                categorias.pop(categorias.index(removCategoria))
                                csv.salvarCSV(DIRETORIOS["categorias"], categorias, 'categoria')
                                print(f"\n\n{CORES['VERDE']}A categoria {CORES['NEGRITO']}{removCategoria}{CORES['RESET']} {CORES['VERDE']}foi removida!")
                            else: # se não existir a categoria, avisar
                                print(f'{CORES["VERMELHO"]}A categoria {CORES["NEGRITO"]}{removCategoria}{CORES["RESET"]}{CORES["VERMELHO"]} não se encontra na lista de categorias!{CORES["RESET"]}')
                            input(f"{CORES['RESET']}\nPressione Enter para continuar...")
                        case '0':
                            break
                        case _:
                            input(f"Opção inválida!\nPressione Enter para tentar novamente...")
            case '3':
                while True:
                    limparTerminal()
                    print(f"{CORES['VERDE']}=== CofreSeguro ==={CORES['RESET']}")
                    print(f"{CORES['ITALICO']}Você está no menu de {CORES['NEGRITO']}registro de auditoria.{CORES['RESET']}") # o famigerado log!!111!


                    print(f'\n\n{CORES["NEGRITO"]}Opções:{CORES["RESET"]} \n1. Visualizar registro completo\n2. Visualizar registro por operação\n0. Sair')
                    operacao = input('Digite o número da operação: ')
                    limparTerminal()
                    match operacao:
                        case '1':
                            print(f'Todos os registros: {CORES["CINZA"]}')
                            printarLog(log)
                            input(f'{CORES["RESET"]}\nPressione Enter para continuar...')
                        case '2':
                            operacaoLog = input("Digite a operação para pesquisar nos registros (adicionar/consultar/alterar/apagar): ")
                            print(f'Registros da operação {operacaoLog}: {CORES["CINZA"]}')
                            printarLog(log, operacaoLog)
                            input(f'{CORES["RESET"]}\nPressione Enter para continuar...')
                        case '0':
                            break
                        case _:
                            input(f"Opção inválida!\nPressione Enter para tentar novamente...")
            case '0':
                print("Fechando cofre...")
                break
            case _:
                input(f"Opção inválida!\nPressione Enter para tentar novamente...")
                


if __name__ == "__main__":
    # iniciar o programa
    main()