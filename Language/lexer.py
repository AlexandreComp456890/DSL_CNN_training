
"""Realiza a analise lexica, identificando os tokens da DSL para CNNs."""
import ast
import sys
import ply.lex as lex

# Palavras reservadas da linguagem
reserved = {
    "DATASET": "DATASET",        # Define o conjunto de dados utilizado
    "SPLIT": "SPLIT",            # Divide os dados em treino e validacao
    "MODEL": "MODEL",            # Define a arquitetura do modelo
    "CNN": "CNN",                # Identifica uma rede neural convolucional
    "TRAIN": "TRAIN",            # Configura o treinamento do modelo
    "EVALUATE": "EVALUATE",      # Avalia o desempenho do modelo
    "SAVE": "SAVE",              # Salva o modelo treinado
    "NORMALIZE": "NORMALIZE",    # Normaliza os valores dos dados
    "AUGMENT": "AUGMENT",        # Aplica transformacoes nos dados de treino

    # Camadas da CNN
    "CONV": "CONV",              # Camada convolucional que extrai caracteristicas
    "RELU": "RELU",              # Funcao de ativacao que introduz nao linearidade
    "POOL": "POOL",              # Reduz as dimensoes dos mapas de caracteristicas
    "FLATTEN": "FLATTEN",        # Converte os dados em um vetor unidimensional
    "DENSE": "DENSE",            # Camada totalmente conectada de neuronios
    "DROPOUT": "DROPOUT",        # Desativa neuronios aleatoriamente no treinamento

    # Valores booleanos
    "true": "TRUE",              # Representa o valor booleano verdadeiro
    "false": "FALSE",            # Representa o valor booleano falso
}

# Tokens reconhecidos pelo analisador lexico
tokens = [
    "ID",                       # Identificadores e nomes de parametros
    "CTE_INT",                  # Constantes numericas inteiras
    "CTE_FLOAT",                # Constantes numericas decimais
    "CTE_STRING",               # Textos e caminhos entre aspas
    "IGUAL",                    # Simbolo de atribuicao (=)
    "PONTO_VIRGULA",            # Indica o fim de uma instrucao (;)
    "ABRE_CHAVE",               # Indica o inicio de um bloco ({)
    "FECHA_CHAVE",              # Indica o fim de um bloco (})
] + list(reserved.values())      # Adiciona as palavras reservadas aos tokens

# Simbolos da linguagem
t_IGUAL = r"="
t_PONTO_VIRGULA = r";"
t_ABRE_CHAVE = r"\{"
t_FECHA_CHAVE = r"\}"

# Caracteres ignorados durante a analise
t_ignore = " \t\r"

# Ignora comentarios iniciados por # ou //
def t_COMENTARIO(t):
    r"\#[^\n]*|//[^\n]*"
    pass

# Reconhece strings e interpreta caracteres escapados
def t_CTE_STRING(t):
    r'"([^"\\\n]|\\["\\nt])*"'

    t.value = ast.literal_eval(t.value)
    return t

# Reconhece numeros decimais e notacao cientifica
def t_CTE_FLOAT(t):
    r"-?(?:(?:\d+\.\d*|\.\d+)(?:[eE][+-]?\d+)?|\d+[eE][+-]?\d+)"

    t.value = float(t.value)
    return t

# Reconhece constantes numericas inteiras
def t_CTE_INT(t):
    r"-?\d+"

    t.value = int(t.value)
    return t

# Reconhece identificadores e palavras reservadas
def t_ID(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"

    t.type = reserved.get(t.value, "ID")
    return t

# Atualiza a contagem de linhas do codigo
def t_newline(t):
    r"\n+"

    t.lexer.lineno += len(t.value)

# Identifica caracteres invalidos e informa sua localizacao
def t_error(t):
    linha = t.lineno

    coluna = (
        t.lexpos
        - t.lexer.lexdata.rfind("\n", 0, t.lexpos)
    )

    raise SyntaxError(
        f"Erro lexico na linha {linha}, "
        f"coluna {coluna}: "
        f"caractere {t.value[0]!r}"
    )

# Cria uma nova instancia do analisador lexico
def criar_lexer():
    """Cria e retorna um analisador lexico configurado para a DSL."""

    analisador = lex.lex(module=sys.modules[__name__])
    analisador.lineno = 1

    return analisador
