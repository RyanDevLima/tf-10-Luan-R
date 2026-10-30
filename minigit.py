from collections import deque

class MiniGit:
    """
    Classe que simula um sistema de controle de versão simplificado (MiniGit).
    Gerencia commits, branches e merges armazenando o histórico na forma de um grafo.
    """
    
    __slots__ = [
        '__pais', 
        '__mensagens', 
        '__branches', 
        '__branch_atual', 
        '__contador_commits', 
        '__passos'
    ]

    def __init__(self):
        """
        Inicializa um repositório Git vazio na branch 'main'.
        Nenhum passo é contabilizado na inicialização.
        """
        self.__pais = {}             # commit -> lista dos commits pais
        self.__mensagens = {}        # commit -> string da mensagem
        self.__branches = {}         # branch -> commit para onde aponta
        self.__branch_atual = "main" # Nome da branch em uso
        self.__contador_commits = 0  # Contador sequencial para os IDs (c1, c2...)
        self.__passos = 0            # Armazena os passos da última operação

    @property
    def passos(self):
        """
        Property somente de leitura para obter os passos da última operação executada.
        """
        return self.__passos

    @property
    def branch_atual(self):
        """
        Property somente de leitura para obter o nome da branch atual.
        """
        return self.__branch_atual

    def commitar(self, mensagem):
        """
        Cria um novo commit na branch atual.
        Gasta fixamente 2 passos (1 para criar o commit + 1 para mover a branch).
        """
        if not mensagem:
            raise ValueError("A mensagem do commit não pode ser vazia.")
            
        self.__contador_commits += 1
        novo_identificador = f"c{self.__contador_commits}"
        
        self.__mensagens[novo_identificador] = mensagem
        self.__pais[novo_identificador] = []
        
        commit_atual = self.__branches.get(self.__branch_atual)
        if commit_atual:
            self.__pais[novo_identificador].append(commit_atual)
            
        self.__branches[self.__branch_atual] = novo_identificador
        self.__passos = 2
        return novo_identificador

    def mensagem(self, commit):
        """
        Retorna a mensagem de um commit específico buscando direto no dicionário.
        Gasta fixamente 1 passo de leitura.
        """
        if commit not in self.__mensagens:
            raise ValueError("Commit inexistente.")
            
        self.__passos = 1
        return self.__mensagens[commit]

    def pais(self, commit):
        """
        Retorna os pais de um commit convertidos para uma tupla imutável.
        Gasta fixamente 1 passo de leitura.
        """
        if commit not in self.__pais:
            raise ValueError("Commit inexistente.")
            
        self.__passos = 1
        return tuple(self.__pais[commit])

    def criar_branch(self, nome):
        """
        Cria uma nova branch apontando para o commit da branch atual.
        Gasta fixamente 1 passo (1 ponteiro criado).
        """
        commit_atual = self.__branches.get(self.__branch_atual)
        if not commit_atual:
            raise ValueError("Não é possível criar branch em um repositório sem commits.")
            
        if nome in self.__branches:
            raise ValueError("Uma branch com este nome já existe.")
            
        self.__branches[nome] = commit_atual
        self.__passos = 1

    def trocar_branch(self, nome):
        """
        Altera a branch ativa do repositório.
        Gasta fixamente 1 passo (1 ponteiro de controle movido).
        """
        if nome not in self.__branches:
            raise ValueError("Branch inexistente.")
            
        self.__branch_atual = nome
        self.__passos = 1

    def mesclar(self, nome):
        """
        Realiza a mesclagem da branch indicada na branch atual, gerando um commit com dois pais.
        Gasta fixamente 2 passos (1 para criar o commit + 1 para mover a branch).
        """
        if nome not in self.__branches:
            raise ValueError("Branch indicada para merge não existe.")
            
        if nome == self.__branch_atual:
            raise ValueError("Não é possível mesclar uma branch nela mesma.")
            
        self.__contador_commits += 1
        novo_identificador = f"c{self.__contador_commits}"
        
        self.__mensagens[novo_identificador] = f"merge de {nome}"
        
        pai_atual = self.__branches[self.__branch_atual]
        pai_mesclado = self.__branches[nome]
        self.__pais[novo_identificador] = [pai_atual, pai_mesclado]
        
        self.__branches[self.__branch_atual] = novo_identificador
        self.__passos = 2
        return novo_identificador

    def log(self):
        """
        Percorre o histórico a partir do commit atual de forma em largura usando uma fila.
        Gasta 1 passo por commit visitado e inserido na tupla final.
        """
        commit_inicial = self.__branches.get(self.__branch_atual)
        if not commit_inicial:
            self.__passos = 0
            return ()
            
        visitados = []
        fila = deque([commit_inicial])
        
        while fila:
            atual = fila.popleft()
            if atual not in visitados:
                visitados.append(atual)
                for pai in self.__pais[atual]:
                    fila.append(pai)
                    
        self.__passos = len(visitados)
        return tuple(visitados)

    def buscar(self, texto):
        """
        Busca sequencial por um commit cuja mensagem contenha o texto informado.
        Gasta 1 passo para cada commit inspecionado em ordem cronológica de criação.
        """
        passos_gastos = 0
        for i in range(1, self.__contador_commits + 1):
            identificador = f"c{i}"
            passos_gastos += 1
            if texto in self.__mensagens[identificador]:
                self.__passos = passos_gastos
                return identificador
                
        self.__passos = passos_gastos
        return None

    def merges(self):
        """
        Filtra e retorna todos os commits que possuem mais de um pai.
        Gasta fixamente 1 passo por commit existente no repositório inteiro.
        """
        lista_merges = []
        for i in range(1, self.__contador_commits + 1):
            identificador = f"c{i}"
            if len(self.__pais[identificador]) > 1:
                lista_merges.append(identificador)
                
        self.__passos = self.__contador_commits
        return tuple(lista_merges)

def tentar(acao):
    try:
        acao()
    except ValueError as erro:
        print("erro:", erro)

# --- Cenário de Testes (Passo 7) ---
git = MiniGit()
git.commitar("primeiro commit")
print(git.passos)
git.commitar("segundo commit")
git.criar_branch("feature")
print(git.passos)
git.commitar("terceiro commit")
git.trocar_branch("feature")
git.commitar("quarto commit")
git.trocar_branch("main")
git.mesclar("feature")
print(git.pais("c5"))
print(git.log(), git.passos)
print(git.mensagem("c3"), git.passos)
print(git.buscar("quarto"), git.passos)
print(git.merges())
git.trocar_branch("feature")
print(git.log(), git.passos)
git.trocar_branch("main")

# Testes que devem falhar
tentar(lambda: git.trocar_branch("inexistente"))
tentar(lambda: git.criar_branch("main"))
tentar(lambda: git.mesclar("main"))
tentar(lambda: git.pais("c99"))


# --- Função Medir (Passo 8) ---
def medir(quantidade):
    git_medicao = MiniGit()
    for i in range(quantidade):
        git_medicao.commitar(f"commit {i}")
    passos_escrita = git_medicao.passos
    git_medicao.log()
    passos_leitura = git_medicao.passos
    return passos_escrita, passos_leitura

print("\ncommits | passos do commitar | passos do log")

for qtd in [10, 100, 1000,]:
    
    escrita, leitura = medir(qtd)
    print(f"{qtd:<7} | {escrita:<19} | {leitura}")
