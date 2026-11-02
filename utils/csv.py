# biblioteca caseira que vai ter as funções pra criar e alterar os csv desse lindo projeto
# e também pro main.py não ficar cheio de baboseira num arquivo só

# TO DO!!! adicionar um esquema em que nos csv, se perceba quando tem aspas entre os valores, 
# porque, quando se tem, é uma "falsa virgula", 
# isto é, dentro de algum valor, mais provavelmente na observação, tem uma virgula que não determina um novo valor,
# mas sim, uma virgula usual, como a de gramática
# é preciso se atentar a isso porque o esquema de ler os csv é justamente dar o split em virgulas

from datetime import datetime
import os

def carregarCSV(qual, ehLista = False):
    data = {}
    dataL = []
    chaves = []
    estaLendoChaves = True # na primeira linha, tem as chaves do dicionario, essa variavel serve pra dizer que ta lendo as chaves, e depois que lê, fica falsa, e daí se le os valores!

    if os.path.isfile(qual): # ver se o csv existe, se não, ele cria um vazio
        with open(qual, 'r', encoding='UTF-8') as csv:
            csv = csv.read()
            if len(csv) != 0:
                if csv[-1] == '\n': # se tiver a merda de uma quebra de linha sobrando no csv, essa função quebra e faz tudo se tornar uma lista vazia...
                    csv = csv[0:-1]
                for linha in csv.split('\n'):
                    dados = linha.split(',')
                    if estaLendoChaves:
                        chaves = dados
                        estaLendoChaves = False
                    else:
                        if len(dados) == 1: # quando só tem uma coluna, isso é uma lista apenas, e nao um dicionario
                            dataL.append(dados[0])
                            data = dataL
                        else:
                            for i in range(len(dados)):
                                # [dados[0]]?? = o primeiro indice de qualquer linha guarda a chave pai do dicionario de valores, no caso do cofre:
                                # o primeiro indice é o nome do serviço, ele quem vai ser usado pra resgatar os outros dados (senha, categoria)

                                # já os outros indices equivalem cada um a suas chaves, isso sao justamente as colunas do csv. por isso o [chaves[i]]
                                if ehLista:
                                    if i == 0:
                                        dataL.append({}) # inicializar um novo dicionario pra guardar o dados dessa linha, ja que nesse caso, é disposto por dicionarios em uma lista
                                    dataL[-1][chaves[i]] = dados[i]
                                else:
                                    if i == 0:
                                        data[dados[0]] = {} # inicializar a tal chave pai
                                        continue
                                    data[dados[0]][chaves[i]] = dados[i]
    else: # criar um csv vazio, já que tentou carregar um arquivo que nao existe
        with open(qual, 'w', encoding='UTF-8') as csv:
                csv.write('')
    if ehLista:
        data = dataL
    return data



def salvarCSV(onde,data: dict,chavePai=None): # essa função se baseia muito na expectativa de que o usuario vai escrever todos os dicionarios estritamente iguais e na ordem correta por causa da chave, se nao houver nenhuma modificação por fora, o cofreseguro consegue essa expectativa
    chaves = []
    if len(data) == 0: # se nn tem nada no dicionario pra salvar, entao  nao salva nada ne
        with open(onde, 'w', encoding='UTF-8') as csv:
            csv.write('')
        return
    
    with open(onde, 'w', encoding='UTF-8') as csv:

        if type(data) == dict:
            csv.write(chavePai)
            for chave in list(data.values())[0].keys(): # pegar um dicionario de exemplo pra que ele monte o cabeçalho de colunas, por exemplo: servico,credencial,senha,classe,registro,obs
                csv.write(f",{chave}")
                chaves.append(chave)

            csv.write('\n') 
            for valorPrin, dados in data.items(): # agora sim guardar os dados
                csv.write(valorPrin) # escrever o valor que no dicionario é a chave pai, no exemplo do login, o nome do serviço é quem se refere ao dicionario de dados, por isso ele fica separado da variavel dados
                for chave in chaves:
                    csv.write(','+dados[chave])
                csv.write('\n')

        elif type(data) == list: # no caso do log, nao precisamos de uma chave pai, já que o registro são varios dicionarios em uma lista só, sem uma chave principal para referencia-los
            if chavePai is not None: # quando a data a ser salva é uma lista, e tem uma chave pai, é porque a data é uma lista de strings, por exemplo, a lista de categorias (categorias = ['Jogos', 'Diversão']), não há nenhuma chave além do nome da variável em si
                csv.write(chavePai)
                csv.write('\n') 
                for dado in data:
                    csv.write(dado)
                    csv.write('\n')
            else:

                for chave in data[0].keys(): # matheuzinho, espero que tu entenda o resto e comente pra mim !!
                    chaves.append(chave)
                    
                    if chave == list(data[0].keys())[0]:
                        csv.write(f"{chave}")    
                        continue
                    csv.write(f",{chave}")

                csv.write('\n') 
                for dados in data:
                    for chave in chaves:
                        if chave == chaves[0]:
                            csv.write(dados[chave])
                            continue
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

def registrarLog(onde, log:list, operacao,oqueMudou):
    # tabela:
    # operacao,quando,alteracoes

    # Se apagarmos todas as senhas essa vai ser a mensagem
    if oqueMudou == "Todas as senhas":
        alteracoes = f"({operacao.upper()}) Todas as senhas foram apagadas."
    else:
        # montar a frasezinha: tal coisa foi alterada, por exemplo: (ADICIONAR) A senha do serviço Reddit foi adicionada.'
        alteracoes = f"({operacao.upper()}) A senha do serviço {oqueMudou} foi {operacao[0:len(operacao)-1]}da."


    log.insert(0, {
        'operacao': operacao,
        'quando': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        'alteracoes': alteracoes
    })
    salvarCSV(onde, log)
    print(f'\n\033[3m\033[90mAtualização no Registro de Auditoria: {alteracoes}\033[0m')
    return log