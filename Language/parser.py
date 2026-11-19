"""Realiza a analise sintatica dos comandos da DSL para CNNs."""
import sys
import ply.yacc as yacc
from .lexer import tokens
from .nodes import Camada, Comando, Modelo, Programa

# Define o ponto inicial da gramatica e cria a AST do programa
def p_programa(p):
    "programa : instrucoes"

    p[0] = Programa(instrucoes=p[1])

# Inicia a lista de instrucoes com um unico comando
def p_instrucoes_uma(p):
    "instrucoes : instrucao"

    p[0] = [p[1]]

# Adiciona novas instrucoes a lista existente
def p_instrucoes_varias(p):
    "instrucoes : instrucoes instrucao"

    p[0] = p[1] + [p[2]]

# Define os tipos de instrucoes aceitos pela linguagem
def p_instrucao(p):
    """instrucao : comando_dataset
                | comando_config
                | comando_model
                | comando_evaluate
                | comando_save"""

    p[0] = p[1]

# Reconhece a declaracao de um dataset
def p_comando_dataset(p):
    "comando_dataset : DATASET origem PONTO_VIRGULA"

    tipo, valor = p[2]

    p[0] = Comando(
        nome="DATASET",
        parametros={
            "tipo": tipo,
            "valor": valor
        }
    )

# Identifica se a origem e um dataset conhecido ou um diretorio
def p_origem(p):
    """origem : ID
              | CTE_STRING"""

    if p.slice[1].type == "ID":
        tipo = "catalogo"
    else:
        tipo = "diretorio"

    p[0] = (tipo, p[1])

# Reconhece os comandos de configuracao e seus parametros
def p_comando_config(p):
    """comando_config : SPLIT parametros PONTO_VIRGULA
                      | TRAIN parametros PONTO_VIRGULA
                      | NORMALIZE parametros PONTO_VIRGULA
                      | AUGMENT parametros PONTO_VIRGULA"""

    p[0] = Comando(
        nome=p[1],
        parametros=p[2]
    )

# Reconhece a definicao do modelo e suas camadas
def p_comando_model(p):
    "comando_model : MODEL CNN ABRE_CHAVE camadas FECHA_CHAVE"

    p[0] = Modelo(
        tipo="CNN",
        camadas=p[4]
    )

# Inicia a lista de camadas do modelo
def p_camadas_uma(p):
    "camadas : camada"

    p[0] = [p[1]]

# Adiciona novas camadas a arquitetura do modelo
def p_camadas_varias(p):
    "camadas : camadas camada"

    p[0] = p[1] + [p[2]]

# Reconhece camadas que exigem parametros
def p_camada_parametrizada(p):
    """camada : CONV parametros PONTO_VIRGULA
              | POOL parametros PONTO_VIRGULA
              | DENSE parametros PONTO_VIRGULA
              | DROPOUT parametros PONTO_VIRGULA"""

    p[0] = Camada(
        nome=p[1],
        parametros=p[2]
    )

# Reconhece camadas que nao recebem parametros
def p_camada_simples(p):
    """camada : RELU PONTO_VIRGULA
              | FLATTEN PONTO_VIRGULA"""

    p[0] = Camada(
        nome=p[1],
        parametros={}
    )

# Reconhece o comando de avaliacao do modelo
def p_comando_evaluate(p):
    "comando_evaluate : EVALUATE ID PONTO_VIRGULA"

    p[0] = Comando(
        nome="EVALUATE",
        parametros={
            "conjunto": p[2]
        }
    )

# Reconhece o caminho utilizado para salvar o modelo
def p_comando_save(p):
    "comando_save : SAVE CTE_STRING PONTO_VIRGULA"

    p[0] = Comando(
        nome="SAVE",
        parametros={
            "caminho": p[2]
        }
    )

# Inicia o dicionario de parametros com um unico elemento
def p_parametros_um(p):
    "parametros : parametro"

    nome, valor = p[1]

    p[0] = {nome: valor}

# Adiciona parametros e impede nomes duplicados
def p_parametros_varios(p):
    "parametros : parametros parametro"

    nome, valor = p[2]

    if nome in p[1]:
        raise ValueError(
            f"Parametro repetido: {nome!r}"
        )

    p[0] = {
        **p[1],
        nome: valor
    }

# Reconhece parametros no formato nome=valor
def p_parametro(p):
    "parametro : ID IGUAL valor"

    p[0] = (p[1], p[3])

# Reconhece valores inteiros, decimais, strings e identificadores
def p_valor(p):
    """valor : CTE_INT
             | CTE_FLOAT
             | CTE_STRING
             | ID"""

    p[0] = p[1]

# Converte os valores booleanos para True ou False
def p_valor_booleano(p):
    """valor : TRUE
             | FALSE"""

    p[0] = (p[1] == "true")

# Identifica erros de sintaxe e informa a linha do problema
def p_error(p):
    if p is None:
        raise SyntaxError(
            "Erro sintatico: fim inesperado do arquivo"
        )

    raise SyntaxError(
        f"Erro sintatico na linha {p.lineno}: "
        f"token {p.type} com valor {p.value!r}"
    )

# Cria e configura o analisador sintatico utilizando o PLY
def criar_parser():
    """Cria e retorna uma instancia do analisador sintatico."""

    return yacc.yacc(
        module=sys.modules[__name__],
        start="programa",
        write_tables=False,
        debug=False
    )
