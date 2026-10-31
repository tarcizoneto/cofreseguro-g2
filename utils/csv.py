# biblioteca caseira que vai ter as funções pra criar e alterar os csv desse lindo projeto
# e também pro main.py não ficar cheio de baboseira num arquivo só

# TO DO!!! adicionar um esquema em que nos csv, se perceba quando tem aspas entre os valores, 
# porque, quando se tem, é uma "falsa virgula", 
# isto é, dentro de algum valor, mais provavelmente na observação, tem uma virgula que não determina um novo valor,
# mas sim, uma virgula usual, como a de gramática
# é preciso se atentar a isso porque o esquema de ler os csv é justamente dar o split em virgulas

def carregarCSV(qual):
    data = {}
    dataL = []
    chaves = []
    chavePrincipal = ''
    estaLendoChaves = True # na primeira linha, tem as chaves do dicionario, essa variavel serve pra dizer que ta lendo as chaves, e depois que lê, fica falsa, e daí se le os valores!


    with open(qual, 'r', encoding='UTF-8') as csv:
        csv = csv.read()
        for linha in csv.split('\n'):
            dados = linha.split(',')
            if estaLendoChaves:
                chaves = dados
                estaLendoChaves = False
            else:
                if len(dados) == 1: # quando só tem uma coluna, isso é uma lista apenas, e nao um dicionario
                    dataL.append(dados)
                    data = dataL
                else:
                    for i in range(len(dados)):
                        # [dados[0]]?? = o primeiro indice de qualquer linha guarda a chave pai do dicionario de valores, no caso do cofre:
                        # o primeiro indice é o nome do serviço, ele quem vai ser usado pra resgatar os outros dados (senha, categoria)

                        # já os outros indices equivalem cada um a suas chaves, isso sao justamente as colunas do csv. por isso o [chaves[i]]
                        if i == 0:
                            data[dados[0]] = {} # inicializar a tal chave pai
                            continue
                        data[dados[0]][chaves[i]] = dados[i]
    return data



def salvarCSV(onde,dicionario: dict,chavePai): # essa função se baseia muito na expectativa de que o usuario vai escrever todos os dicionarios estritamente iguais e na ordem correta por causa da chave, se nao houver nenhuma modificação por fora, o cofreseguro consegue essa expectativa
    chaves = []
    with open(onde, 'w', encoding='UTF-8') as csv:
        csv.write(chavePai)
        for chave in list(dicionario.values())[0].keys(): # pegar um dicionario de exemplo pra que ele monte o cabeçalho de colunas, por exemplo: servico,credencial,senha,classe,registro,obs
            csv.write(f",{chave}")
            chaves.append(chave)

        csv.write('\n') 
        for valorPrin, dados in dicionario.items(): # agora sim guardar os dados
            csv.write(valorPrin) # escrever o valor que no dicionario é a chave pai, no exemplo do login, o nome do serviço é quem se refere ao dicionario de dados, por isso ele fica separado da variavel dados
            for chave in chaves:
                csv.write(','+dados[chave])
            csv.write('\n')




# tipos de log:
# adicionar
# alterar
# consultar
# exemplo de csv:
# operacao,quando,alteracoes
# alterar,30-10-2026 13:13,senha do banco tal foi alterada
# consulta, 30-10-2026 13:14, senha do jogo tal foi revelada

def registrarLog(operacao,mudancas):
    # fica pra amanha baby
    pass