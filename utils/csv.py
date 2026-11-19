# biblioteca caseira que vai ter as funções pra criar e alterar os csv desse lindo projeto
# e também pro main.py não ficar cheio de baboseira num arquivo só




from datetime import datetime
import os


def quebrarLinhacomVirgulasFalsas(linha): 
    dados = [''] # ja deixar o primeiro indice inicializado
    indiceAtualDados = 0


    # variaveis de acontecimentos
    if linha[0] != '"': # se a linha nao começar com aspas, é pra ja começar o for lendo alguma variável
        lendoVariavel = True
    else:
        lendoVariavel = False
    ignorandoVirgulas = False  
    ignorandoAspas = False
    
    for idxCaractere in range(len(linha)): # ler caractere por caractere e ir adicionando toda vez que acharmos um valor
#                                            acredito  que tenha um jeito mais fácil de fazer isso, se tiver, me avisem
        
        caractere = linha[idxCaractere]


        match caractere:
            case '"':
                if ignorandoAspas:
                    ignorandoAspas = False
                    dados[indiceAtualDados] += '"' # precisamos de todo jeito adicionar as aspas, ja que foi ignorada ESTRUTURALMENTE, e não como parte da string
                else:
                    if not ignorandoVirgulas: # se nao tiver com uma variavel aberta
                        ignorandoVirgulas = True # agora, qualquer virgula (que agora tao dentro de uma variavel) precisa ser ignorada
                    else:
                        ignorandoVirgulas = False # e se tiver com a variavel aberta (ignorando virgulas), eh pq nao precisa mais ignorar, a variavel acabou

                
            case ',':
                if ignorandoVirgulas: 
                    dados[indiceAtualDados] += ',' # precisamos de todo jeito adicionar as virgulas, ja que foi ignorada ESTRUTURALMENTE, e não como parte da string
                else:
                    indiceAtualDados += 1
                    dados.append('')
                    # if linha[idxCaractere+1] == '"': # ver se o prpoximo faractere eh uma aspa pra saber se vai abrir uma coisa diferente
                    #     ignorandoVirgulas = True

            case '\\':
                ignorandoAspas = True # isso aqui >>\"<< eh quando vai ter uma aspas dentro da variavel, por exemplo uma senha que usa aspas como caractere especial
            case _: # se o caractere nao for sobre nada de estrutura, adicionar como um caractere na variavel que ta lendo agora, ne
                if lendoVariavel:
                    dados[indiceAtualDados] += caractere
                
    print(dados)
    return dados

def formatarValorCSV(chave:str): # criei essa função pra toda vez que for salvar chave/valor no csv, essa belezinha vai e
#                                    verifica se tem algum caracter especial que possa quebrar a leitura, se tiver, ajusta a chave e retorna ela bonitinha
    if '"' in chave:
        chave = chave.replace('"', '\\"')
    if ',' in chave:
        chave = f'"{chave}"'

    return chave


def carregarCSV(qual, ehLista = False):
    data = {}
    dataL = []
    chaves = []
    estaLendoChaves = True # na primeira linha, tem as chaves do dicionario, essa variavel serve pra dizer que ta lendo as chaves, e depois que lê, fica falsa, e daí se le os valores!

    if os.path.isfile(qual): # ver se o csv existe, se não, ele cria um vazio
        with open(qual, 'r', encoding='UTF-8') as csv:
            csv = csv.read()
            if len(csv) != 0:
                if csv[-1] == '\n': # se tiver a merda de uma quebra de linha sobrando no csv, essa função quebra e faz tudo se tornar uma lista vazia... ajeitando isso
                    csv = csv[0:-1]
                for linha in csv.split('\n'):

                    if linha.count('"') >= 2: # se tiver mais de duas aspas (mais de uma, porque pode se ter uma aspa dentro do valor) numa linha, quer dizer que vai ter alguma variável com vírgula, 
#                                               e essa virgula não é pra separar valores, mas sim uma virgula dentro de um valor,
#                                               por isso que precisa dividir de outro jeito, se usássemos split ia separar por vírgulas
#                                               inclusive a virgula que nao era pra ser dividida.
                        dados = quebrarLinhacomVirgulasFalsas(linha)
                        
                    else: # se nao tiver nenhuma virgula que vai quebrar erroneamente, isto é, não tiver mais de duas aspas (que indicam valores com virgulas dentro), pode dar split normalmente
                        dados = linha.split(',') # dividir a linha em valores. no csv, o valor eh separado por virgulas

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

                                # if dados[i][0] == '"' and dados[i][-1] == '"': 

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
                csv.write(formatarValorCSV(valorPrin)) # escrever o valor que no dicionario é a chave pai, no exemplo do login, o nome do serviço é quem se refere ao dicionario de dados, por isso ele fica separado da variavel dados
                for chave in chaves:
                    csv.write(','+formatarValorCSV(dados[chave]))
                csv.write('\n')

        elif type(data) == list: # no caso do log, nao precisamos de uma chave pai, já que o registro são varios dicionarios em uma lista só, sem uma chave principal para referencia-los
            if chavePai is not None: # quando a data a ser salva é uma lista, e tem uma chave pai, é porque a data é uma lista de strings, por exemplo, a lista de categorias (categorias = ['Jogos', 'Diversão']), não há nenhuma chave além do nome da variável em si
                csv.write(chavePai)
                csv.write('\n') 
                for dado in data:
                    csv.write(dado)
                    csv.write('\n')
            else: # se for uma lista simples, como o log, sem chave pai

                for chave in data[0].keys(): # matheuzinho, espero que tu entenda o resto e comente pra mim !! ... nem eu (tarcizo) lembro
                    chaves.append(chave)
                    
                    if chave == list(data[0].keys())[0]: # só pra deixar o ritmo do write + ",chave"  por isso a gente vê a primeira e não escreve a virgula de separação, ja que eh a primeira
                        csv.write(f"{chave}")    
                        continue
                    csv.write(f",{chave}") # e daqui em diante, pode seguir dando ,chave

                csv.write('\n') 
                for dados in data:
                    for chave in chaves:
                        if chave == chaves[0]:
                            csv.write(formatarValorCSV(dados[chave]))
                            continue
                        csv.write(','+formatarValorCSV(dados[chave]))
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
    if operacao == 'IA':
        alteracoes = f"(IA) PROMPT: \"{oqueMudou}\""
    else:
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

