# MiniGit - Análise de Estrutura de Dados e Complexidade

Tabela comparativa gerada através da medição de operações:

| commits | passos do commitar | passos do log |
| :---    | :---               | :---          |
| 10      | 2                  | 10            |
| 100     | 2                  | 100           |
| 1000    | 2                  | 1000          |

### Perguntas e Respostas

**1. Por que o commitar gasta sempre 2 passos, e o log gasta mais conforme o histórico cresce?**
O método `commitar` faz uma operação de escrita direta associando chaves e valores e alterando o ponteiro da branch, o que leva um tempo constante independente do tamanho do repositório. Já o `log` necessita caminhar por todo o grafo mapeando os relacionamentos retroativamente, o que exige visitar cada nó individualmente e faz o custo crescer proporcionalmente ao tamanho do histórico.

**2. Por que mensagem(commit) gasta 1 passo e buscar(texto) pode gastar muitos? O que o dicionário ganha quando se procura pela chave, e o que ele não ajuda quando se procura pelo valor?**
Buscar por chave no dicionário ativa o mecanismo de hashing interno, indo direto ao endereço de memória em um único passo. Quando procuramos pelo valor interno através do método `buscar`, o dicionário perde essa vantagem competitiva e somos forçados a realizar uma busca sequencial analisando registro por registro até encontrar o termo desejado.

**3. Por que o merge é um commit com dois pais, e por que isso faz do histórico um grafo, e nao uma lista?**
O merge une duas linhas temporais de desenvolvimento distintas que vinham acontecendo paralelamente. Ao criar uma conexão para dois commits pais simultaneamente, o fluxo deixa de ser uma sequência linear estrita (lista) e passa a bifurcar e convergir em múltiplos caminhos estruturais (grafo).

**4. Por que o método pais devolve uma tupla, e não a lista que está guardada dentro do dicionário?**
Retornar a lista interna daria uma referência direta para a estrutura mutável interna da classe, permitindo alterações externas maliciosas ou acidentais fora do controle do MiniGit. Ao converter para uma tupla, protegemos a integridade dos dados por se tratar de uma estrutura de dados imutável.
