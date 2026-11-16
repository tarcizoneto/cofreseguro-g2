from utils import seguranca
# importando da biblioteca para ler o arquivo de senhas de outros serviços


# Função para detectar risco de reutilização de senhas
def verificar_senhas_repetidas(senha, cofre, servicoIgnorado=None):

    # Percorre os serviços cadastrados no cofre anteriormente (exemplo shopee,reddit..)
    for servico in cofre:

        # rejeita o serviço atual durante uma alteração
        if servico == servicoIgnorado:
            continue

        # acessa a senha armazenada no serviço
        senhaSalva = cofre[servico]['senha']

        # compara a senha digitada com a senha cadastrada
        if senha == senhaSalva:

            print(
                "Risco identificado! Essa senha já está "
                "sendo utilizada no serviço {servico}."
            )

            return True

    # caso termine o laço sem encontrar repetição
    return False




    
