 **COFRESEGURO🔐 Grupo 2:**

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

### Menu Principal:
```
    1. Adicionar credencial
    2. Listar credenciais
    3. Editar credencial
    4. Excluir credencial
    5. Revelar senha
    6. Gerenciar categorias
    7. Verificar senhas repetidas
    8. Relatório de segurança
    9. Consultar log de auditoria

```
## <span style="color: salmon;">Níveis:</span> 

|  Fraca:

|  Média:

|  Forte:
### Detecção de reutilização

Se a mesma senha aparece em mais de um serviço, o sistema lista todos eles.
Isso importa porque, se um serviço vazar, **todos os outros que compartilham
a senha ficam expostos**. 
