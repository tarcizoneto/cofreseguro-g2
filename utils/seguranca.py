# Sistema de segurança de senhas:

# - Criar função na qual importa o cofre e o log
# - Escaneia todas as senhas e separa em uma lista
# - A lista será usada para a verificação da segurança de cada uma. 

# Utilização de condicionais:
# - Cria-se 4 variáveis com alfabeto maiúsculo, alfabeto minúsculo, algarismos numéricos e caracteres especiais
# as variáveis serão checadas nos if's.

# criar um for para verificar senha por senha e dentro desse for, cria-se outro for para verificar os caracteres.
# criar um contador para verificar quantos caracteres de cada se tem, e se eles estão bem distribuídos.

# A segurança das senhas deve conter condições que definam a facilidade de decifrá-las.

import os
import csv
from datetime import datetime
import random
import secrets

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


# Separação dos caracteres em strigs 

minus = 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,á,é,í,ó,ú,à,è,ì,ò,ù,â,ê,ô,û,ã,õ,ñ,ç'.split(",")
maius = 'A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,Á,É,Í,Ó,Ú,À,È,Ì,Ò,Ù,Â,Ê,Ô,Û,Ã,Õ,Ñ,Ç'.split(",")
nums = '1,2,3,4,5,6,7,8,9,0'.split(",")
especiais = '!,@,#,$,%,&,*,_,>,<,^,~,;,:,?,/,\\,-,{,},[,],\',"'.split(",")

def segura_senha(senha, senhasComuns, printarForca = True):
    #Importação das senhas comuns e definição dos contadores
    forca_da_senha = None
    cont_minus = 0
    cont_maius = 0
    cont_nums = 0
    cont_esp = 0
    cont_difs = 0
    cont_reps = 0

    # Contagem dos caracteres
    senha_contada = ""
    for caracteres in senha:
        if caracteres not in senha_contada:
            cont_difs += 1
        senha_contada += caracteres
        if senha.count(caracteres) > cont_reps:
            cont_reps = senha.count(caracteres)
        if caracteres in minus:
            cont_minus += 1
        if caracteres in maius:
            cont_maius += 1
        if caracteres in nums:
            cont_nums += 1
        if caracteres in especiais:
            cont_esp += 1

    # print(cont_difs)
    # print(cont_reps)

    # Soma dos caracteres após a contagem
    cont_caracteres = len(senha)

    # Checagem de força da senha


    # Criação de variáveis das condições: 
    condi_forte = cont_caracteres >= 10 and cont_esp != 0 and cont_minus != 0 and cont_maius != 0 and cont_nums != 0 and cont_difs >= 8 and cont_reps <= 10
    condi_media = cont_caracteres >= 8 and cont_maius != 0 and cont_nums != 0 and cont_difs >= 5



    if cont_caracteres <= 5:
        if printarForca:
            print(f'{CORES["VERMELHO"]}Senha fraquíssima... Tenha mais criatividade :P{CORES["RESET"]}')
        forca_da_senha = "Fraquíssima"

    elif senha in senhasComuns:
        if printarForca:
            print(f'{CORES["VERMELHO"]}Esta é uma senha {CORES["NEGRITO"]}extremamente comum.{CORES["RESET"]}{CORES["VERMELHO"]} Tente outra!{CORES["RESET"]}')
        forca_da_senha = "Fraquíssima"

    elif condi_forte:
        if printarForca:
            print(f'{CORES["VERDE"]}Senha forte o suficiente!{CORES["RESET"]}')
        forca_da_senha = "Forte"

    elif condi_media:
        if printarForca:
            print(f'{CORES["AMARELO"]}Senha média. Recomenda-se uma mais forte!{CORES["RESET"]}')
        forca_da_senha = "Média"

    else:
        if printarForca:
            print(f'{CORES["VERMELHO"]}Senha fraca. Tente uma senha mais forte!{CORES["RESET"]}')
        forca_da_senha = "Fraca"

    if printarForca:
        
        if forca_da_senha == 'Fraquíssima' or forca_da_senha == 'Fraca' or forca_da_senha == 'Média':
            verificar = input(f"Gostaria de verificar as condições que {CORES['NEGRITO']}fortificam a senha? {CORES['RESET']}{CORES['ITALICO']}(SIM/NÃO){CORES['RESET']}: ").upper()
        

            if verificar == "SIM":
    # Verificação de confições
                print(f"\n===============================================================")

                if cont_caracteres >= 10:
                    print(f'\n{CORES["NEGRITO"]}➜  A condição "Pelo menos 10 caracteres" é:\t     {CORES["VERDE"]}válida{CORES["RESET"]}')
                else:
                    print(f'\n{CORES["NEGRITO"]}➜  A condição "Pelo menos 10 caracteres" é:\t     {CORES["VERMELHO"]}inválida{CORES["RESET"]}')

                
                if cont_esp != 0:
                    print(f'{CORES["NEGRITO"]}➜  A condição "Possui caracteres especiais" é:\t     {CORES["VERDE"]}válida{CORES["RESET"]}')
                else:
                    print(f'{CORES["NEGRITO"]}➜  A condição "Possui caracteres especiais" é:\t     {CORES["VERMELHO"]}inválida{CORES["RESET"]}')

                
                if cont_minus != 0:
                    print(f'{CORES["NEGRITO"]}➜  A condição "Possui letras minúsculas" é:\t     {CORES["VERDE"]}válida{CORES["RESET"]}')
                else:
                    print(f'{CORES["NEGRITO"]}➜  A condição "Possui letras minúsculas" é:\t     {CORES["VERMELHO"]}inválida{CORES["RESET"]}')
                
                if cont_maius != 0:
                    print(f'{CORES["NEGRITO"]}➜  A condição "Possui letras maiúsculas" é:\t     {CORES["VERDE"]}válida{CORES["RESET"]}')
                else:
                    print(f'{CORES["NEGRITO"]}➜  A condição "Possui letras maiúsculas" é:\t     {CORES["VERMELHO"]}inválida{CORES["RESET"]}')

                if cont_nums != 0:
                    print(f'{CORES["NEGRITO"]}➜  A condição "Possui números " é:\t             {CORES["VERDE"]}válida{CORES["RESET"]}')
                else:
                    print(f'{CORES["NEGRITO"]}➜  A condição "Possui números" é:\t              {CORES["VERMELHO"]}inválida{CORES["RESET"]}')

                if cont_reps <= 10:
                    print(f'{CORES["NEGRITO"]}➜  A condição "Até 10 caracteres repetidos" é:\t     {CORES["VERDE"]}válida{CORES["RESET"]}')
                else:
                    print(f'{CORES["NEGRITO"]}➜  A condição "Até 10 caracteres repetidos" é:\t     {CORES["VERMELHO"]}inválida{CORES["RESET"]}')

                if cont_difs >= 8:
                    print(f'{CORES["NEGRITO"]}➜  A condição "No mínimo 8 caracteres diferentes" é: {CORES["VERDE"]}válida{CORES["RESET"]}')
                else:
                    print(f'{CORES["NEGRITO"]}➜  A condição "No mínimo 8 caracteres diferentes" é: {CORES["VERMELHO"]}inválida{CORES["RESET"]}')
                
                print(f"\n===============================================================\n")
            
            # if verificar == "NAO" or verificar == "NÃO" : # no caso, nao precisa printar nada pq ja volta p função la de mudar a senha
            #     print("")

    return forca_da_senha

#Biblioteca reservada pra detecção de risco

# Função para detectar risco de reutilização de senhas
def verificar_senhas_repetidas(senha, cofre):

    # Lista de serviços com senhas repetidas
    servSenhasRepet = []

    # Percorre os serviços cadastrados no cofre anteriormente (exemplo shopee,reddit..)
    for servico,dados in cofre.items():

        # acessa a senha armazenada no serviço
        senhaSalva = cofre[servico]['senha']

        # Adiciona o serviço da senha repetida na lista
        if senha == senhaSalva:
            servSenhasRepet.append(servico)

    if len(servSenhasRepet) != 0:
        print(f'\n{CORES["NEGRITO"]}{CORES["VERMELHO"]}RISCO IDENTIFICADO{CORES["RESET"]}')
        print(f'Essa senha já está sendo utilizada em {CORES["NEGRITO"]}{CORES["VERMELHO"]}{len(servSenhasRepet)}{CORES["RESET"]} Serviços: {CORES["AMARELO"]}{servSenhasRepet}{CORES["RESET"]}')
        print(f'{CORES["ITALICO"]}Considere trocar senhas repetidas para mais segurança!!!{CORES["RESET"]}\n')
        return True
    # caso termine o laço sem encontrar repetição
    return False


def gerar_senha(tamanho=12): #definição do tamanho ao colocar uma senha
    while True:
        if tamanho < 12:
            print(f"\n===============================================\n")
            raise ValueError("O tamanho recomendado é 12 caracteres.") #nega a inserção da senha ao colocar menos do que 12 caracteres
            
        #garante pelo menos um caractere de cada tipo da lista feita
        senhas = [secrets.choice(minus),
                secrets.choice(maius),
                secrets.choice(nums),
                secrets.choice(especiais)
        ]
        #Preenche o restante da senha aleatoriamente
        todos_caracteres = minus + maius + nums + especiais
        senhas += [secrets.choice(todos_caracteres)for _ in range(tamanho - 5)]

        #Embaralha e gera uma senha na lista de modo aleatório
        secrets.SystemRandom().shuffle(senhas)

        nova_senha = "".join(senhas)

        
        if segura_senha(nova_senha, [], False) == 'Forte':
            break
        else:
            print("Senha insegura gerada: ", nova_senha)
        
    print("Senha gerada:", nova_senha)


# feito com tarcizo e matheuzinho - ideia princiapl foi de matheus

def criptografar_senha(senha, repeticoes):
    qtdLinhas = int(-(-(len(senha)**0.5)//1))
    qtdColunas = int(len(senha)**0.5)
    print(f'linhas: {qtdLinhas}, colunas: {qtdColunas}')

    matriz = []
    for linha in range(qtdLinhas):
        matriz.append([])
        for coluna in range(qtdColunas):
            indiceCaractereAtual = linha*qtdColunas + coluna
            if indiceCaractereAtual < len(senha):
                matriz[linha].append(senha[indiceCaractereAtual])
            else:
                matriz[linha].append('fs')

    sal = ""
    for linha in range(qtdLinhas):
        for coluna in range(qtdColunas):
            print(matriz[linha][coluna], end=' ')
        print('')

    for i in range(repeticoes):
        linhaOUcoluna = random.randint(0,1)
        print(linhaOUcoluna)
        if linhaOUcoluna == 0:
            linhaComeco = random.randint(0,qtdLinhas-1)
            while True:
                linhaFim = random.randint(0,qtdLinhas-1)
                if linhaFim != linhaComeco:
                    break
            print(f'Linha {linhaComeco} vai pra linha {linhaFim}')
            linha1 = matriz[linhaComeco]
            linha2 = matriz[linhaFim]
            matriz[linhaComeco] = linha2
            matriz[linhaFim] = linha1
            sal = str(linhaOUcoluna) + str(linhaFim) + str(linhaComeco) + sal
        else:
            colunaComeco = random.randint(0,qtdColunas-1)
            while True:
                colunaFim = random.randint(0,qtdColunas-1)
                if colunaFim != colunaComeco:
                    break
            
            print(f'Coluna {colunaComeco} vai para coluna {colunaFim}')
            listaColunaComeco = []
            listaColunaFim = []
            for linha in range(qtdLinhas): # primeiro guardar os valores pra depois trocar
                for coluna in range(qtdColunas):
                    if coluna == colunaComeco:
                        listaColunaComeco.append(matriz[linha][coluna])
                    elif coluna == colunaFim:
                        listaColunaFim.append(matriz[linha][coluna])

            for linha in range(qtdLinhas):
                matriz[linha][colunaComeco] = listaColunaFim[linha]
                matriz[linha][colunaFim] = listaColunaComeco[linha]
            
            sal = str(linhaOUcoluna) + str(colunaFim) + str(colunaComeco) + sal

        for linha in range(qtdLinhas):
                for coluna in range(qtdColunas):
                    print(matriz[linha][coluna], end=' ')
                print('')


        senhaNova = ''

        for linha in range(qtdLinhas):
            for coluna in range(qtdColunas):
                senhaNova += matriz[linha][coluna] + '¨'
        senhaNova = senhaNova[0:-1]

        print(sal)
        print(senhaNova)
    return sal, senhaNova
        

def descriptografar_senha(sal, senhaCriptografada):
    senha = senhaCriptografada.split('¨')
    print(senha)
    
    qtdLinhas = int(-(-(len(senha)**0.5)//1))
    qtdColunas = int(len(senha)**0.5)
    print(f'linhas: {qtdLinhas}, colunas: {qtdColunas}')

    matriz = []
    for linha in range(qtdLinhas):
        matriz.append([])
        for coluna in range(qtdColunas):
            indiceCaractereAtual = linha*qtdColunas + coluna
            matriz[linha].append(senha[indiceCaractereAtual])


    for linha in range(qtdLinhas):
        for coluna in range(qtdColunas):
            print(matriz[linha][coluna], end=' ')
        print('')
    for i in range(int(len(sal)/3)):

        linhaOUcoluna = int(sal[i*3])

        if linhaOUcoluna == 0:
            linhaComeco = int(sal[i*3+1])
            linhaFim = int(sal[i*3+2])


            print(f'Linha {linhaComeco} vai pra linha {linhaFim}')
            linha1 = matriz[linhaComeco]
            linha2 = matriz[linhaFim]
            matriz[linhaComeco] = linha2
            matriz[linhaFim] = linha1
        else:
            colunaComeco = int(sal[i*3+1])
            colunaFim = int(sal[i*3+2])
            
            print(f'Coluna {colunaComeco} vai para coluna {colunaFim}')
            listaColunaComeco = []
            listaColunaFim = []
            for linha in range(qtdLinhas): # primeiro guardar os valores pra depois trocar
                for coluna in range(qtdColunas):
                    if coluna == colunaComeco:
                        listaColunaComeco.append(matriz[linha][coluna])
                    elif coluna == colunaFim:
                        listaColunaFim.append(matriz[linha][coluna])

            for linha in range(qtdLinhas):
                matriz[linha][colunaComeco] = listaColunaFim[linha]
                
                matriz[linha][colunaFim] = listaColunaComeco[linha]
            

        for linha in range(qtdLinhas):
                for coluna in range(qtdColunas):
                    print(matriz[linha][coluna], end=' ')
                print('')


        senhaDes = ''

        for linha in range(qtdLinhas):
            for coluna in range(qtdColunas):
                if matriz[linha][coluna] != 'fs':
                    senhaDes += matriz[linha][coluna]

    return senhaDes
        




# matriz = [
#     [1, 2, 3, 4],
#     [5, 6, 7, 8],
#     [9, 10, 11, 12],
#     [13, 14, 15, 16]
# ]
# senha = 123456789



sal, senha = criptografar_senha('CatimbalDoParafuso1245@%#%$@$fs', 5)

print('sSENHA DESCRIPOGROAFADADA:  '+descriptografar_senha(sal, senha))
print(f"SENHA CRIPTOGRAFADA: ", senha)
print(f'SAL USADO: '+sal)

# quando tem por exemplo, 13 caracteres e a matriz só cobre 12, um fica de fora, fazer com que o alcance 9linahas e colunas cubra até o excedente