 **COFRESEGURO Grupo 2:**

 # <span style="color: Orange; ">*Manual do usuário:</span>*

 ### Gerenciador de Credenciais Didático em *Python*, feito para organizar senhas, entender sua força e enxergar riscos como senhas repetidas e fracas e sua segurança de modo geral.

**AVISO IMPORTANTE**: a utilização de senhas que você usa no dia a dia não é recomendado para a utilização do cofre, senhas como: ~~04072007~~ referentes a data de nascimento ou algo do tipo.

O **CofreSeguro** ajuda o usuário a organizar suas credenciais, entender a
força de cada senha e enxergar esses riscos.

## <span style="color: Lightblue;">Funcionamento:</span> 


- **Categorias:** banco, rede social, estudo, trabalho, você pode implementar de sua escolha dentre jogos, sites pra lazer educação, trabalho e outros, cada uma adicionada pelo próprio usuário
- **Senhas mascaradas:** a listagem mostra só os 2 primeiros caracteres
  seguidos de asteriscos; há uma opção específica para revelar a senha.
- **Força de senha:** classifica a senha em fraca, média ou forte e
  **explica o motivo** da classificação.
-  **Lista de senhas comuns:** avisa se a senha consta em `senhasComuns.csv`
-  **Detecção de risco:** alerta quando a mesma senha é usada em mais de um
serviço e mostra quais serviços.
- **Registro de auditoria:** exibe todas as operações relevantes (**inclusive revelar
  uma senha**) são gravadas em `log.csv` com operação, serviço afetado, data e hora

### Menu principal:
```
1. Senhas
2. Categorias
3. Registro de Auditoria
0. Sair

```
```
Menu de senhas: 

1. Adicionar senha
2. Consultar senha
3. Alterar senha
4. Apagar senha
5. Listar senhas
6. Listar senhas por categoria
7. Apagar todas as senhas (USE COM CUIDADO)
0. Sair

```
## Detecção de reutilização

Se a mesma senha aparece em mais de um serviço, o sistema mostra a quantidade e lista o nome desses serviços com a mesma senha, além de recomendar a troca de senhas.
Isso importa porque, se um serviço vazar, **todos os outros que compartilham
a mesma senha ficam vulneráveis**. 

## <span style="color:LightBlue;">Gerador de senhas:</span>

#### O sistema funciona como um gerador aleatório de recomendação para a força de senha com o objetivo de selecionar uma criptografia segura para os diversos tipos de serviços que o usuário quiser inserir suas senhas

  ## 1.1 - Instruções de utilização:

  1 - Inicie o main.py com python3 para iniciar o programa

  2 - Selecione o menu desejado para começar as ações

  3 - Selecione a ação à ser feita em cada menu

  4 - Preencha os dados na ação selecionada

  5 - O sistema armazenará as informações cadastradas 
  
  6 - Pressione **Enter** para sair da ação

  ## 1.2 - Adição de senhas:
O sistema, ao criar uma senha o sistema pede 5 informações principais que são
- **O serviço desejado**
- **A credencial/Usuário do serviço**
- **A senha de modo geral**
- **A Categoria em que o serviço se  enquadra**
- **Uma observação opcional**

*Logo após inserir as informações as informações serão armazenadas no `cofre.csv`*

## <span style="color: salmon;"> Verificador de níveis de senha:</span> 

## Forte: ---> 
Pelo menos 10 caracteres, conter caracteres especiais, letras minusculas e maiusculas, numeros e mais de 8 caracteres diferentes e menos de 10 caracteres iguais.
## Média: --->
Pelo menos 8 caracteres, conter caracteres maiusculos, minusculos e numeros com pelo menos 5 caracteres diferentes.
## Fraca: --->
Todas as senhas que não seguem as condições acima.
## Fraquissima: -->
Todas as senhas dentro do nosso acervo de senhas comuns e senhas com até 5 caracteres.

 ## 1.3 - Consulta de senhas:
  Após inserir a senha no serviço desejado o sistema verificará a senha e irá mostrar o usuário se ele deseja visualizar a senha caso a tenha a esquecido.

 1 -  O sistema vai deslocar o usuário para uma seleção de serviços 

2 - O sistema vai no dicionário do cofre buscar a senha do serviço.

3 - O sistema irá mostrar a senha específica do serviço desejado

## 1.4 - Alteração de senhas:
Após a consulta de senhas mostrar os serviços o sistema irá perguntar se deseja atualizar a senha de determinado serviço.

1 - O sistema vai deslocar para o menu de senhas. 

2 - O sistema vai perguntar se deseja atualizar a senha.

3 - Clique em **Editar** senha.

## 1.5 - Apagar senhas:

Após inserir ou alterar determinada senha do serviço escolhido o sistema irá instruir baseado no seu interesse se voce deseja apagar sua senha.

1 - O sistema irá deslocar o usuário para o menu de senhas. 

2 - O usuário irá selecionar qual serviço ele deseja apagar.

3 - Clique em **Apagar** senha.

## 1.6 - Listar senhas:
O sistema agora irá deslocar para a aba de serviços que possuem uma senha e irá mover o usuário para visualizar todas as senhas que os serviços possuem. 

1 - O sistema ira mover o usuário para um gerenciador de senhas.

2 - O sistema ira mostrar as os serviços e suas determinadas chaves.

3 - O sistema vai mostrar todas as senhas dos serviços que você cadastrou.

## 1.7 Listar senhas por categoria:

Da mesma forma que foi feito na instrução anterior o sistema irá direcionar o usuário para uma lista de senhas pelo serviço desejado.

1 - O sistema ira mover o usuário para um gerenciador de senhas.

2 - O sistema ira mostrar as os serviços e suas determinadas chaves.

3 - O sistema irá mostrar todas as senhas do serviço em específico e todas as outras cadastradas.

## 1.8 Apagar todas as senhas <span style="color:RED;">*USE COM CUIDADO*:</span> 

1 - Se o usuário deseja apagar as senhas o sistema irá direcionar para remover todas as senhas cadastradas.

2 - O sistema irá perguntar se o usuário deseja mesmo remover todas as senhas perguntando. **SIM/NÃO**

3 - Depois de Clicar **SIM** o sistema irá remover todas as senhas cadastradas.


