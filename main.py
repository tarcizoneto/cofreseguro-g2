import os
from utils import csv
from datetime import datetime
from utils import seguranca

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




# essa função serviria caso a gente não tivesse um csv para salvar as categorias, e daí precisaríamos buscar as categorias ao percorrer todas as senhas,
# mas agora, nós salvamos as categorias em csv.
# def acharCategorias(cofre):
#     categorias = []
#     for servico in cofre.values():
#         if servico['categoria'] not in categorias:
#             if 'categoria' in servico:
#                 categorias.append(servico['categoria'])
#     return categorias


# ~ tarcizo
# para deixar documentada a minha indignação e o que eu vou mudar:
# Carol tinha me dito que é mais intuitivo separar cada ação do crude em funções, só que, o meu raciocínio é que: 
# pra facilitar a vida da manipulação de variáveis, o mais prático é deixar tudo num escopo de uma função só, e só manipular a variável cofre
# "por que tem praticidade nisso?" -> vejamos, quando se separa o crude por funções, cada função (adicionar, excluir, alterar), vai mexer diretamente no dicionario cofre
# e pra se ter esse dicionario em TODAS as funções, vai precisar passar o dicionario como argumento, e depois de mexer no dicionario, vai precisar retornar o dicionario, pra na linha que chamar essa função, atribuir o dicionario alterado no escopo na função main
# |-> trabalho de corno não só pra fazer, mas pra explicar também

# "e como que você fez então?" --> eu deixei tudo na função main, com o "bloco de código", como carol contestou, e, usando match e os cases, que vê qual ação o usuário quer fazer, e as ações diretamente nos casos
#                                  dentro de cada caso, já se roda tudo que é preciso fazer, chamando apenas funções que foram criadas para evitar repetições (como salvar o csv, ler o csv, printar as categorias)

# "uai, mas o intuito do projeto é se ter funções..." -> e tem, porém só quando é realmente necessário. 
# 
# "tá, mas e se separarmos de todo jeito?" -> no crude, por exemplo, seria mais trabalhoso ainda separar todas as ações em funções,
#                                             ficaria mais legível? mais ou menos. mas, a que custo? ficaria difícil de entender porque tantos returns e tantas atribuições. 
# |-> entendam, separar todas as ações em funções pra cada deixaria a forma que Vitor fez o crude em sala muito mais prática: (função adicionar = lê o arquivo, adiciona, salva o arquivo), porque, dentro dessas funções, ele lê o arquivo e trabalha com todas as variáveis necessárias no escopo da função.
# mas entendam também o problema que existe nessa técnica: funções existem justamente para deixar o MÍNIMO de repetição no código, 
# é CANSATIVO pro programa e pro código abrir o arquivo toda vez, recriar o dicionario de senhas TODA VEZ pra poder mexer numa mínima coisa?!
# é mais facil de entender? É!! mas já cabe ao estudante saber e pensar alto: imaginem só, a demora que ia ser pra carregar um arquivo que tem 1000 senhas, e precisar carregar TUDO ISSO só pra REMOVER uma, uuuma ínfima senha...
# o melhor jeito é: abrir no começo, deixar uma variável global rodando do programa, e não carregar mais csv nenhum, e só salvar o csv quando alterar algo nele.

# como vou fazer, pra ter mais ainda o requisito de "funções": separar com aquele trabalho de corno de atribuir e informar o dicionario toda vez que for alterar numa função, e deixar TODAS as ações separadas... contra minha vontade...




# FUNÇÕES DO MENU SENHA

def senha_adicionar(cofre, log):
    print(f'{CORES["ITALICO"]}Você está adicionando uma senha, deixe o nome do serviço em branco para sair... {CORES["RESET"]}\n') # uma ótima funcionalidade é pra que, caso o usuario queira sair e não quer realmente adicionar uma senha, só precisa deixar em branco
    servico = input('Digite o nome de serviço no qual essa senha está sendo usada: ').strip().capitalize()
    if servico == '': # o programa vê se ta em branco, e se tiver, é porque o usuario quer sair
        return cofre, log, False # entao a gente sai
    elif servico in cofre:
        input(f"\n\nEsse serviço {CORES['NEGRITO']}já tem uma senha cadastrada!{CORES['RESET']}")
        return cofre, log, False
    while True:
        cred = input("Digite a credencial (usuário, e-mail ou login) dessa senha: ").strip()
        if cred: # se a credencial nao estiver vazia, entao foi validada, eh show
            break
        # se estiver vazia, o loop continua e printa esse aviso aqui embaixo
        print(f"{CORES['VERMELHO']}A credencial precisa ter {CORES['NEGRITO']}pelo menos um caractere!{CORES['RESET']}\n")


    while True: 
        senha = input("Digite a senha: ").strip() # todo: alguma forma de criptografia
        fortitude = seguranca.segura_senha(senha, senhasC)

        if fortitude == 'Média':
            continuar = input(f"Deseja continuar com essa senha, {CORES['ITALICO']}mesmo tendo segurança média?{CORES['RESET']} {CORES['ITALICO']}(SIM/NÃO){CORES['RESET']}: ").upper()
            if continuar == "SIM": 
                break

            else: # se o usuario digitar "nao", ou so deixar em branco, é pra digitar de novo
                continue
        
        if fortitude == 'Forte':
            break
        

    if len(categorias) > 0: # só se pode escolher uma categoria pra senha se existirem categorias, se nao tiver nenhuma por enquanto
            print(f"\nCategorias disponíveis:{CORES['CINZA']}")
            printarCategorias(categorias)
            while True: # loop basiquinho pra forçar o usuário a digitar uma categoria válida, se o número não estiver no alcance, ele repete até estar
                categoria = input(f"{CORES['RESET']}Digite a categoria desejada com base na lista acima (de 1 a {len(categorias)}, {CORES['ITALICO']}ou deixe em branco para não categorizar{CORES['RESET']}): ")
                if categoria == '': # se o usuario nao tiver escrito nada, vamos entender que ele quis deixar a senha sem categoria.
                    
                    break
                if categoria.isdigit(): # vamos ver se o numero que o usuario digitou pode se transformar em número, se nao, nem tenta converter pra int
                    categoria = int(categoria) - 1 # se eh um numero valido, entao converte e diminui um pra transformar o número em indice
                    if categoria < 0 or categoria > (len(categorias) - 1): # agora validar o número ne, se ta no alcance esperado
                        print(f'{CORES["VERMELHO"]}Categoria inválida, digite um número de 1 a {len(categorias)}.{CORES["RESET"]}') # olha aí, digite um numero de 1 até 4, por exemplo, se tiver 4 categorias
                    else: # se tiver no alcance, para o loop porque já temos um numero valido pra categoria
                        break
                else:
                    print(f'{CORES["VERMELHO"]}Entrada inválida, digite um número VÁLIDO de 1 a {len(categorias)}.{CORES["RESET"]}')
            if categoria == '':
                categoriaEscolhida = '-' # categoria vazia
            else:
                categoriaEscolhida = categorias[categoria] # categoria válida\

    else:
        categoriaEscolhida = '-'
        print(f"{CORES['CINZA']}{CORES['ITALICO']}Não existe nenhuma categoria, altere a senha em outro momento para atribuir esse serviço a uma.{CORES['RESET']}")
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

    print(f"\n\n{CORES['VERDE']}Senha do serviço {CORES['NEGRITO']}{servico}{CORES['RESET']} {CORES['VERDE']}adicionada com sucesso!{CORES['RESET']}")
    return cofre, log, True
                                
def senha_consultar(cofre, log):
    print(f'{CORES["ITALICO"]}Você está consultando uma senha, deixe o nome do serviço em branco para sair... {CORES["RESET"]}')

    printarServicos(cofre) # pra printar os serviços                                                                                          kk

    servico = input('Digite o nome do serviço da senha que você deseja consultar: ').strip().capitalize()
    if servico == '':
        return cofre, log, False

    if servico in cofre:
        log = csv.registrarLog(DIRETORIOS['log'], log, 'consultar', servico)
        print(f"\n{CORES['VERDE']}A credencial do serviço \"{servico}\" é {CORES['NEGRITO']}{cofre[servico]['credencial']}{CORES['RESET']}{CORES['VERDE']}, e sua senha é {CORES['NEGRITO']}{manipularSenha('visualizar', cofre[servico]['senha'])}{CORES['RESET']}.")
        
    else:
        print(f"\n{CORES['VERMELHO']}Esse serviço {CORES['NEGRITO']}não está no cofre{CORES['RESET']}{CORES['VERMELHO']}, verifique se você o digitou certo ou se ainda não adicionou-o.")

    return cofre, log, True
    
def senha_alterar(cofre, log):
    print(f'{CORES["ITALICO"]}Você está alterando uma senha, deixe o nome do serviço em branco para sair... {CORES["RESET"]}')

    printarServicos(cofre) # pra printar os serviços                                                                                          kk

    servico = input(f'Digite o nome do serviço da senha que você deseja alterar: ').strip().capitalize()
    if servico == '':
        return cofre, log, False

    if servico in cofre:
        cred = input(f"Digite a nova credencial (usuário, e-mail ou login) dessa senha{CORES['ITALICO']}, ou deixe em branco para manter{CORES['RESET']}: ").strip() # esse negocio fresca
        
        while True: 
            senha = input(f"Digite a nova senha{CORES['ITALICO']}, ou deixe em branco para manter{CORES['RESET']}: ").strip() # todo: alguma forma de criptografia
            if senha == '':
                break
            fortitude = seguranca.segura_senha(senha, senhasC)

            if fortitude == 'Média':
                continuar = input(f"Deseja continuar com essa senha, {CORES['ITALICO']}mesmo tendo segurança média?{CORES['RESET']} {CORES['ITALICO']}(SIM/NÃO){CORES['RESET']}: ").upper()
                if continuar == "SIM": 
                    break

                else: # se o usuario digitar "nao", ou so deixar em branco, é pra digitar de novo
                    continue
            
            if fortitude == 'Forte':
                break
            

        if len(categorias) > 0: # só se pode escolher uma categoria pra senha se existirem categorias, se nao tiver nenhuma por enquanto
                print(f"\nCategorias disponíveis:{CORES['CINZA']}")
                printarCategorias(categorias)
                while True: # loop basiquinho pra forçar o usuário a digitar uma categoria válida, se o número não estiver no alcance, ele repete até estar
                    categoria = input(f"{CORES['RESET']}Digite a nova categoria desejada com base na lista acima (de 1 a {len(categorias)}, {CORES['ITALICO']}ou deixe em branco para não categorizar{CORES['RESET']}): ")
                    if categoria == '': # se o usuario nao tiver escrito nada, vamos entender que ele quis deixar a senha sem categoria.
                        break
                    if categoria.isdigit(): # vamos ver se o numero que o usuario digitou pode se transformar em número, se nao, nem tenta converter pra int
                        categoria = int(categoria) - 1 # se eh um numero valido, entao converte e diminui um pra transformar o número em indice
                        if categoria < 0 or categoria > (len(categorias) - 1): # agora validar o número ne, se ta no alcance esperado
                            print(f'{CORES["VERMELHO"]}Categoria inválida, digite um número de 1 a {len(categorias)}.{CORES["RESET"]}') # olha aí, digite um numero de 1 até 4, por exemplo, se tiver 4 categorias
                        else: # se tiver no alcance, para o loop porque já temos um numero valido pra categoria
                            break
                    else:
                        print(f'{CORES["VERMELHO"]}Entrada inválida, digite um número VÁLIDO de 1 a {len(categorias)}.{CORES["RESET"]}')
                if categoria == '':
                    categoriaEscolhida = '-' # categoria vazia
                else:
                    categoriaEscolhida = categorias[categoria] # categoria válida

        else:
            categoriaEscolhida = '-'
            print(f"{CORES['CINZA']}{CORES['ITALICO']}Não existe nenhuma categoria, crie uma e altere a senha novamente para atribuir este serviço à ela.{CORES['RESET']}")
        observacao = input(f"Digite uma nova observação para essa senha {CORES['ITALICO']}(ou deixe em branco, caso não queira alterar){CORES['RESET']}: ")
        horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if observacao == '': # se nao tiver nada a ser observado
            observacao = '-'
        
        if cred != "":
            cofre[servico]['credencial'] = cred
        if senha != "":
            cofre[servico]['senha'] = manipularSenha('registrar', senha)
        if categoriaEscolhida != "":
            cofre[servico]['categoria'] = categoriaEscolhida
        if observacao != "":
            cofre[servico]['obs'] = observacao

        if senha != "" or cred != "":
            cofre[servico]['registro'] = horario
            log = csv.registrarLog(DIRETORIOS['log'], log, 'alterar', servico)

        csv.salvarCSV(DIRETORIOS["cofre"], cofre, 'servico')

        print(f"\n{CORES['VERDE']}O serviço \"{servico}\" foi {CORES['NEGRITO']}alterado!{CORES['RESET']}") # printyt kk
    else:
        print(f"\nEsse serviço {CORES['NEGRITO']}não está no cofre{CORES['RESET']}, verifique se você o digitou certo ou se ainda não adicionou-o.")

    return cofre, log, True

def senha_apagar(cofre, log):
    print(f'{CORES["ITALICO"]}Você está apagando uma senha, deixe o nome do serviço em branco para sair... {CORES["RESET"]}')

    printarServicos(cofre) # pra printar os serviços                                                                                          kk

    servico = input('Digite o nome do serviço da senha que você deseja apagar: ').strip().capitalize()
    if servico == '':
        return cofre, log, False

    if servico in cofre:
        
        cofre.pop(servico)
        log = csv.registrarLog(DIRETORIOS['log'], log, 'apagar', servico)
        print(f"\n{CORES['VERDE']}A senha do serviço \"{servico}\" foi {CORES['NEGRITO']}apagada!{CORES['RESET']}")

        csv.salvarCSV(DIRETORIOS["cofre"], cofre, 'servico')
    else:
        print(f"\nEsse serviço {CORES['NEGRITO']}não está no cofre{CORES['RESET']}, verifique se você o digitou certo ou se ainda não adicionou-o.")

    return cofre, log, True

def senha_listarPorCategorias(cofre, categorias):
    if len(categorias) > 0: # pra poder listar as senhas por categorias, se precisa de uma categoria, se a lista de categorias tiver vazia, entao fudeu
        print(f"\nCategorias disponíveis:{CORES['CINZA']}")
        printarCategorias(categorias)
        while True: # loop basiquinho pra forçar o usuário a digitar uma categoria válida, se o número não estiver no alcance, ele repete até estar
            categoriaAnalisada = input(f"{CORES['RESET']}Digite a categoria desejada com base na lista acima (de 1 a {len(categorias)}, {CORES['ITALICO']}ou deixe em branco para sair{CORES['RESET']}): ")
            if categoriaAnalisada == '': # se o usuario nao tiver escrito nada, vamos entender que ele quer sair!!!
                return False
            if categoriaAnalisada.isdigit(): # vamos ver se o numero que o usuario digitou pode se transformar em número, se nao, nem tenta converter pra int
                categoriaAnalisada = int(categoriaAnalisada) - 1 # se eh um numero valido, entao converte e diminui um pra transformar o número em indice
                if categoriaAnalisada < 0 or categoriaAnalisada > (len(categorias) - 1): # agora validar o número ne, se ta no alcance esperado
                    print(f'{CORES["VERMELHO"]}Categoria inválida, digite um número de 1 a {len(categorias)}.{CORES["RESET"]}') # olha aí, digite um numero de 1 até 4, por exemplo, se tiver 4 categorias
                else: # se tiver no alcance, para o loop porque já temos um numero valido pra categoria
                    break
            else:
                print(f'{CORES["VERMELHO"]}Entrada inválida, digite um número VÁLIDO de 1 a {len(categorias)}.{CORES["RESET"]}')
        limparTerminal()
        print(f"Senhas salvas com a categoria {CORES['NEGRITO']}{categorias[categoriaAnalisada]}{CORES['RESET']}: \n")
        printarCofre(cofre, categoriaAnalisada)
        return True
    else: # fudeu
        print(f"{CORES['VERMELHO']}Para se listar senhas por categoria, é preciso que exista {CORES['NEGRITO']}pelo menos uma categoria.")
        return True

def senha_apagarTodasAsSenhas(cofre, log):
    apagar = input(f'{CORES["VERMELHO"]}Você escolheu apagar todas as senhas, escreva {CORES["NEGRITO"]}\"SIM\"{CORES["RESET"]}{CORES["VERMELHO"]} para confirmar ou pressione Enter para sair:{CORES["RESET"]} ').upper()
    if apagar == "SIM":
        cofre = {}
        print(f"As senhas foram apagadas")
        log = csv.registrarLog(DIRETORIOS['log'], log, 'apagar', "Todas as senhas")
        csv.salvarCSV(DIRETORIOS["cofre"], cofre, 'servico')
        return cofre, log, True
    else:
        return cofre, log, False

def printarCofre(cofre, categoriaAnalisar=None): # criamos essa função pra printar as senhas de um dicionario desejado, já que além da listagem normal, tem a listagem entre categorias, ficaria uma bagunça isso jogado duas vezes no código 

    printouSenhas = False # essa variável serve pra verificar se a função printou alguma senha ou não, já que não tem como verificar se existe alguma senha

    if len(cofre) > 0:
        print(f"\n{CORES['NEGRITO']}{'Serviço':>20} {'Credencial':>28} {'Senha':>26} {'Categoria':>16} {'Observação':>40} {CORES['RESET']}") # cabeçalho

        if categoriaAnalisar is not None: # se, na hora que chamarem a função, o programa der a categoria a analisar, como acontece no listar senha por categorias,
                                          # a função entende que tem que caçar as senhas e printar só as que forem da categoria pedida
            for servico, dados in cofre.items():
                if categorias[categoriaAnalisar] == dados['categoria']: # to percorrendo todas as senhas, se esta estiver com a caegoria que eu pedi, entao printa!
                    printouSenhas = True # no momento em que printar uma senha, a variavel se torna true e lá no final, não precisa mais printar que não existe nenhuma senha
                    print(f"{servico:>20} {dados['credencial']:>28} {manipularSenha('previa', dados['senha']):>26} {dados['categoria']:>16} {dados['obs']:>40}")
            if not printouSenhas: # se nao printou nenhuma senha, é porque não tem nenhuma senha com essa categoria.
                print(f"{CORES['VERMELHO']}Não há senhas salvas com essa categoria.{CORES['VERMELHO']}")
        else: # se não, printa logo tudo mesmo
            for servico, dados in cofre.items():
                print(f"{servico:>20} {dados['credencial']:>28} {manipularSenha('previa', dados['senha']):>26} {dados['categoria']:>16} {dados['obs']:>40}")
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

def printarServicos(cofre):
    print(f"\n{CORES['CINZA']}Serviços cadastrados:")
    for i in cofre.keys():
        print(f"    {i}")
    print(CORES["RESET"])

# FUNÇÕES DO MENU CATEGORIA

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

def categoria_adicionar(categorias):
    print(f'{CORES["ITALICO"]}Você está adicionando uma categoria, deixe o nome da categoria em branco para sair... {CORES["RESET"]}\n')
    
    novaCategoria = input("\nDigite a categoria a ser adicionada: ").capitalize().strip()
    if novaCategoria == '':
        return categorias, False

    if novaCategoria not in categorias: # se já nao existir uma categoria, entao eh p adicionar essa
        categorias.append(novaCategoria)
        csv.salvarCSV(DIRETORIOS["categorias"], categorias, 'categoria')
        print(f"\n\n{CORES['VERDE']}A categoria {CORES['NEGRITO']}{novaCategoria}{CORES['RESET']} {CORES['VERDE']}foi adicionada!")
    else: # e avisar se já existe a catgoria
        print(f'{CORES["VERMELHO"]}A categoria {CORES["NEGRITO"]}{novaCategoria}{CORES["RESET"]} {CORES["VERMELHO"]}já se encontra na lista de categorias!{CORES["RESET"]}')
    return categorias, True

def categoria_renomear(categorias, cofre):
    print(f'{CORES["ITALICO"]}Você está renomeando uma categoria, deixe o nome da categoria em branco para sair... {CORES["RESET"]}\n')
                                
    print(f"\nAs categorias atuais são:{CORES['CINZA']}")
    printarCategorias(categorias, mostrarIndices=False)
    removCategoria = input(f"{CORES['RESET']}\nDigite a categoria a ser renomeada: ").capitalize().strip()
    if removCategoria == '':
        return categorias, cofre, False

    while True:
        novoNomeCategoria = input(f"Digite o novo nome para a categoria: ").capitalize().strip()
        if novoNomeCategoria:
            break
        print(f"{CORES['VERMELHO']}A categoria precisa ter {CORES['NEGRITO']}pelo menos um caractere!{CORES['RESET']}\n")

    if removCategoria in categorias: # só renomear se existir, né
        categorias[categorias.index(removCategoria)] = novoNomeCategoria
        cofre = reatribuirServicosACategorias(cofre, removCategoria, novoNomeCategoria)

        csv.salvarCSV(DIRETORIOS["cofre"], cofre, 'servico')
        csv.salvarCSV(DIRETORIOS["categorias"], categorias, 'categoria')
        print(f"\n\n{CORES['VERDE']}A categoria {CORES['NEGRITO']}{removCategoria}{CORES['RESET']} {CORES['VERDE']}foi renomeada para {CORES['NEGRITO']}{novoNomeCategoria}{CORES['RESET']}!")
    else: # se não existir a categoria, avisar
        print(f'{CORES["VERMELHO"]}A categoria {CORES["NEGRITO"]}{removCategoria}{CORES["RESET"]}{CORES["VERMELHO"]} não se encontra na lista de categorias!{CORES["RESET"]}')

    return categorias, cofre, True

def categoria_remover(categorias, cofre):
    print(f'{CORES["ITALICO"]}Você está removendo uma categoria, deixe o nome da categoria em branco para sair... {CORES["RESET"]}\n')
                                
    print(f"\nAs categorias atuais são:{CORES['CINZA']}")
    printarCategorias(categorias, mostrarIndices=False)
    removCategoria = input(f"{CORES['RESET']}\nDigite a categoria a ser removida: ").capitalize().strip()
    if removCategoria == '':
        return categorias, False

    if removCategoria in categorias: # só remover se existir, né
        categorias.pop(categorias.index(removCategoria))
        cofre = reatribuirServicosACategorias(cofre, removCategoria, '-')

        csv.salvarCSV(DIRETORIOS["cofre"], cofre, 'servico')
        csv.salvarCSV(DIRETORIOS["categorias"], categorias, 'categoria')
        print(f"\n\n{CORES['VERDE']}A categoria {CORES['NEGRITO']}{removCategoria}{CORES['RESET']} {CORES['VERDE']}foi removida!")
    else: # se não existir a categoria, avisar
        print(f'{CORES["VERMELHO"]}A categoria {CORES["NEGRITO"]}{removCategoria}{CORES["RESET"]}{CORES["VERMELHO"]} não se encontra na lista de categorias!{CORES["RESET"]}')
    
    return categorias, True

def reatribuirServicosACategorias(cofre, antigaCategoria, novaCategoria): # vejamos, na hora de apagar a categoria, a gente tira lá da lista de categorias, mas e os serviços que tavam atribuidos a essa categoria, essa função é pra deixar esses serviços em branco
#                                                                           e melhor ainda, da pra fazer essa função se adaptar pra renomear as categorias, ja que se renomear, precisa reatribuir os bbdos tambem
    for servico, dados in cofre.items(): # matheuznho, explica a função items p mim, to dementado pra explicar isso eficientemente ~tarcizo
        if antigaCategoria == dados['categoria']: # to percorrendo todas as senhas, se esta estiver com a caegoria que eu pedi, entao troca rs
            cofre[servico]['categoria'] = novaCategoria
    #print(f"{CORES['ITALICO']} Senhas reatribu{CORES['ITALICO']}")  precisa mesmo de um print? parei na metade do caminho pq achei desnê
    return cofre



# FUNÇÕES DO MENU REGISTRO DE AUDITORIA


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

def log_buscarOperacao(log):
    operacaoLog = input(f"Digite a operação para pesquisar nos registros (adicionar/consultar/alterar/apagar), {CORES['ITALICO']}ou deixe em branco para sair{CORES['RESET']}: ")
    if operacaoLog != '':
        print(f'Registros da operação {operacaoLog}: {CORES["CINZA"]}')
        printarLog(log, operacaoLog)
        return True
    return False


# FUNÇÕES PRINCIPAIS

def preparar(): 
    os.system("color && mode con cols=30 lines=30")
    limparTerminal()

    # carregar arquivos necessários
    global cofre, senhasC, log, categorias
    
    cofre = csv.carregarCSV(DIRETORIOS["cofre"])
    senhasC = csv.carregarCSV(DIRETORIOS["senhasCom"])
    log = csv.carregarCSV(DIRETORIOS["log"], ehLista=True)
    categorias = csv.carregarCSV(DIRETORIOS["categorias"], ehLista=True)

def main():
    preparar()
    global cofre, senhasC, log, categorias

    while True:
        limparTerminal()
        print(f"{CORES['VERDE']}=== CofreSeguro ==={CORES['RESET']}")

        print(f'\n\n{CORES["NEGRITO"]}Menus:{CORES["RESET"]} \n1. Senhas\n2. Categorias\n3. Registro de Auditoria\n4. Relatório de Segurança\n0. Sair')
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

                            cofre, log, sucesso = senha_adicionar(cofre, log)
                           
                            if sucesso:
                                input("\nPressione Enter para continuar...")
                        case '2':
                            
                            cofre, log, sucesso = senha_consultar(cofre, log)

                            if sucesso:
                                input('Pressione Enter para continuar...')
                        case '3':

                            cofre, log, sucesso = senha_alterar(cofre, log)

                            if sucesso:
                                input('Pressione Enter para continuar...')
                        case '4':

                            cofre, log, sucesso = senha_apagar(cofre, log)
                            if sucesso:
                                input('Pressione Enter para continuar...')
                        case '5':

                            print("Senhas salvas no CofreSeguro: ")
                            printarCofre(cofre)
                            
                            input('\nPressione Enter para continuar...')
                        case '6':

                            sucesso = senha_listarPorCategorias(cofre, categorias)

                            if sucesso:
                                input(f"{CORES['RESET']}\nPressione Enter para continuar...")
                        case '7':

                            cofre, log, sucesso = senha_apagarTodasAsSenhas(cofre, log)
                            
                            if sucesso:
                                input(f"{CORES['RESET']}\nPressione Enter para continuar...")
                        case '0':
                            break
                        case _:
                            input(f"Opção inválida!\nPressione Enter para tentar novamente...")
            case '2':
                while True:
                    limparTerminal()
                    print(f"{CORES['VERDE']}=== CofreSeguro ==={CORES['RESET']}")
                    print(f"{CORES['ITALICO']}Você está no menu de {CORES['NEGRITO']}categorias.{CORES['RESET']}")

                    
                    print(f'\n\n{CORES["NEGRITO"]}Opções:{CORES["RESET"]} \n1. Adicionar categoria\n2. Remover categoria\n3. Visualizar categorias\n4. Renomear categoria\n0. Sair')
                    operacao = input('Digite o número da operação: ')
                    limparTerminal()
                    match operacao:
                        case '1':

                            categorias, sucesso = categoria_adicionar(categorias)

                            if sucesso:
                                input(f"{CORES['RESET']}\nPressione Enter para continuar...")
                        case '2':
                            
                            categorias, sucesso = categoria_remover(categorias, cofre)
                            
                            if sucesso:
                                input(f"{CORES['RESET']}\nPressione Enter para continuar...")

                           
                        case '3':
                            
                            print(f"As categorias atuais são:{CORES['CINZA']}")
                            printarCategorias(categorias)

                            input(f"{CORES['RESET']}\nPressione Enter para continuar...")

                        case '4':

                            categorias, cofre, sucesso = categoria_renomear(categorias, cofre)
                                                        
                            if sucesso:
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

                            sucesso = log_buscarOperacao(log)
                            if sucesso:
                                input(f'{CORES["RESET"]}\nPressione Enter para continuar...')
                            
                        case '0':
                            break
                        case _:
                            input(f"Opção inválida!\nPressione Enter para tentar novamente...")
            case '4': #relatorio de segurança
                while True:
                    limparTerminal()
                    print(f"{CORES['VERDE']}=== CofreSeguro ==={CORES['RESET']}")
                    print(f"{CORES['ITALICO']}Você está no menu do {CORES['NEGRITO']}Registro de Segurança.{CORES['RESET']}")
                
                                    
                    print(f'\n\n{CORES["NEGRITO"]}Opções:{CORES["RESET"]} \n1. Situação Atual\n0. Sair')
                    operacao = input('Digite o número da operação: ')
                    limparTerminal()
                    match operacao:

                        case '1':
                            total = [] # Percorre os intes de cada serviço no cofre e recolhe apenas as senhas
                            for servico, dados in cofre.items():
                                total.append(dados['senha'])

                            senha_existente = set() # Dando uma pesquisada, descubri que o recurso "set" analisa se há elementos duplicados (conjutos), então ele vê se a senha usada já existe e adiciona no senhas_repetidas que serve meio que um contador de quantas senhas repetidas tem
                            senha_repetida = set()  # Inclusive nos conjuntos se usa add pra adicionar tipo append com lista. Fiquei preso nessa parte pq tava justamente colocando append

                            for senha in total:
                                if senha in senha_existente:
                                    senha_repetida.add(senha) #E Por que isso e não um contdor? Pq se digamos eu coloco 123 em 3 serviços diferentes, isso é só uma senha repetida, mas com o contador leria como 3 senhas repetidas
                                else:
                                    senha_existente.add(senha)

                            medias = 0
                            fortes = 0

                            for senha in total: # Ele olha cada senha da lista e lê qual o tipo de caractere usando o código do seguranca.py
                                minus = sum(1 for c in senha if c in seguranca.minus) # Soma 1 a cada caractere na senha se estiver na lista dos minúsculos e etc
                                maius = sum(1 for c in senha if c in seguranca.maius)
                                nums = sum(1 for c in senha if c in seguranca.nums)
                                esp = sum(1 for c in senha if c in seguranca.especiais)

                                caracteres = minus + maius + nums + esp

                                if caracteres >= 10 and esp != 0 and minus != 0 and maius != 0 and nums != 0:
                                    fortes += 1
                                elif caracteres >= 8 and maius != 0 and nums != 0:
                                    medias += 1

                            if len(senha_existente) == 0:
                                print('==========================================================\nNão existem credenciais cadastradas, vá criar suas senhas!\n==========================================================')
                            else:
                                print(f'Quantidade de credenciais no CofreSeguro: {len(cofre)}\n===========================================')
                                print(f'Quantidade de senhas fortes: {fortes}')

                                if medias >0:
                                    print(f'{CORES['VERMELHO']}(ALERTA){CORES['RESET']} Quantidade de senhas médias: {medias}')
                                if len(senha_repetida) >0:
                                    print(f'{CORES['AMARELO']}(ATENÇÃO){CORES['RESET']} Quantidade de senhas repetidas: {len(senha_repetida)}')

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