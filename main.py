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
log = {}


def manipularSenha(acao, senha): # separei em função os atos de visualizar e criar, ja que em tempos futuros iremos fazer alguma criptografia
    match acao:
        case 'registrar':
            return senha # aqui vai ter o babado todo de criptografar
        case 'visualizar':
            return senha # e aqui vai ter o babado todo de descriptografar
        case _:
            raise ValueError(f'Mal uso da função de manipulação de senhas, {acao} não é uma ação válida')






def preparar(): 
    os.system("color && mode con cols=30 lines=30 && cls")
    # carregar senhas comuns
    cofre = csv.carregarCSV(DIRETORIOS["cofre"])
    senhasC = csv.carregarCSV(DIRETORIOS["senhasCom"])
    log = csv.carregarCSV(DIRETORIOS["log"])

def main():
    preparar()

    while True:
        os.system('cls')
        print(f"{CORES['VERDE']}=== CofreSeguro ==={CORES['RESET']}")

        print(f'\n\n{CORES["NEGRITO"]}Opções:{CORES["RESET"]} \n- Adicionar senha\n- Visualizar senha\n- Trocar senha\n- Excluir senha\n- Listar senhas\n- Registro de Auditoria\n- Sair')
        operacao = input('Digite sua operação [A/V/T/E/L/R/S]: ').upper()
        os.system('cls')
        match operacao:
            case 'A':
                print(f'{CORES["ITALICO"]}Você está adicionando uma senha, deixe o nome do serviço em branco para sair... {CORES["RESET"]}\n')
                servico = input('Digite o serviço no qual essa senha está sendo usada: ')
                if servico == '':
                    continue
                cred = input("Digite a credencial (usuário, e-mail ou login) dessa senha: ")
                senha = input("Digite a senha: ") # todo: alguma forma de criptografia
                classe = input("Digite a categoria dessa credencial: ") # matheuzinho, saiba que depois a gente vai colocar pra ter como criar categorias e referencialas por indice e msotrar todas elas e tudo mais...
                observacao = input(f"Digite uma observação para essa senha {CORES['ITALICO']}(ou deixe em branco, caso não queira){CORES['RESET']}: ")
                horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                cofre[servico] = {
                        'credencial': cred,
                        'senha': manipularSenha('registrar', senha),
                        'classe': classe,
                        'registro': horario
                     }
                if observacao != '': # se tiver algo a ser observado
                    cofre[-1]['obs'] = observacao
                else:
                    cofre[-1]['obs'] = '-'
                # registar no log
                # salvar
                csv.salvarCSV(DIRETORIOS["cofre"], cofre, 'servico')
            case 'V':
                print(f'{CORES["ITALICO"]}Você irá visualizar uma senha, deixe o nome do serviço em branco para sair... {CORES["RESET"]}\n')
                servico = input('Digite o serviço da senha que você deseja visualizar: ')
                if servico == '':
                    continue

                if servico in cofre:
                    print(f"\nA senha do serviço \"{servico}\" é {manipularSenha('visualizar', cofre[servico]['senha'])}.")
                else:
                    print(f"\nEsse serviço ainda não está no cofre, verifique se você o digitou certo ou se ainda não adicionou-o.")

                input('Pressione alguma tecla para continuar...')
            case 'L':
                print(cofre) # só pra testar por enquanto, mas tem que printar direitinho
                input('\nPressione alguma tecla para continuar...')
            case 'S':
                print("Fechando cofre...")
                break


if __name__ == "__main__":
    # Início do programa
    main()
    
    
