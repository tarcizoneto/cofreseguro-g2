
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


minus = 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z'.split(",")
maius = 'A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z'.split(",")
nums = '1,2,3,4,5,6,7,8,9,0'.split(",")
especiais = '!,@,#,$,%,&,*,_'.split(",")

def segura_senha(senha):
    senhasComuns = csv.carregarCSV(DIRETORIOS["senhasCom"])
    forca_da_senha = None
    cont_minus = 0
    cont_maius = 0
    cont_nums = 0
    cont_esp = 0
    cont_pontos = 0

    for caracteres in senha:
        if caracteres in minus:
            cont_minus += 1
        if caracteres in maius:
            cont_maius += 1
        if caracteres in nums:
            cont_nums += 1
        if caracteres in especiais:
            cont_esp += 1
    cont_caracteres = cont_minus + cont_maius + cont_nums + cont_esp

    print(cont_minus)
    print(cont_maius)
    print(cont_esp)
    print(cont_nums)

    if cont_caracteres <= 5:
        print(f'{CORES["VERMELHO"]}Senha fraquíssima...Tenha mais criatividade :P{CORES["RESET"]}')
        forca_da_senha = "Fraquíssima"

    elif senha in senhasComuns:
        print(f'{CORES["VERMELHO"]}Senha fraquíssima...Tenha mais criatividade :P{CORES["RESET"]}')
        forca_da_senha = "Fraquíssima"

    elif cont_minus != 0  and cont_maius != 0 and cont_nums != 0:
        print(f'{CORES["AMARELO"]}Senha Média. Tente uma senha mais forte!{CORES["RESET"]}')
        forca_da_senha = "Média"
    elif cont_caracteres >= 10 and cont_esp != 0 and cont_minus != 0 and cont_maius != 0 and cont_nums != 0:
        print(f'{CORES["VERDE"]}Senha Forte. Tente uma senha mais forte!{CORES["RESET"]}')
        forca_da_senha = "Forte"
    else:
        print(f'{CORES["VERMELHO"]}Senha fraca. Tente uma senha mais forte!{CORES["RESET"]}')
        forca_da_senha = "Fraca"
    return forca_da_senha


teste = input("Digite a senha: ")
print(segura_senha(teste))



 