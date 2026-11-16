
# Função para detectar risco de reutilização de senhas
def verificarSenhasRepetidas(senha, cofre):

    # Percorre os serviços cadastrados no cofre anteriormente (exemplo shopee,reddit..)
    for servico in cofre:
      
        # acessa a senha armazenada no serviço
        senhaSalva = cofre[servico]['senha']

        # compara a senha digitada com a senha cadastrada
        if senha == senhaSalva:

            print(f"Risco identificado! Essa senha já está sendo utilizada no serviço {servico}.")

            return True

    # caso termine o laço sem encontrar repetição
    return False




    
