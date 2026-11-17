import ply.lex as lex

# 1. Palavras reservadas
reserved = {
    "DATASET": "DATASET",
    "SPLIT": "SPLIT",
    "MODEL": "MODEL",
    "CNN": "CNN",
    "TRAIN": "TRAIN"
}

# 2. Lista de tokens
tokens = [
    "ID",
    "CTE_INT",
    "CTE_FLOAT",
    "CTE_STRING",
    "IGUAL",
    "PONTO_VIRGULA"
] + list(reserved.values())


# 3. Símbolos da linguagem
t_IGUAL = r'='
t_PONTO_VIRGULA = r';'


# 4. Ignorar espaços e tabulações
t_ignore = ' \t\r'


# 5. Identificadores e palavras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'

    t.type = reserved.get(t.value, 'ID')
    return t


# 6. Strings
def t_CTE_STRING(t):
    r'"[^"\n]*"'

    t.value = t.value[1:-1]
    return t


# 7. Números decimais
def t_CTE_FLOAT(t):
    r'\d+\.\d+'

    t.value = float(t.value)
    return t


# 8. Números inteiros
def t_CTE_INT(t):
    r'\d+'

    t.value = int(t.value)
    return t


# 9. Nova linha
def t_newline(t):
    r'\n+'

    t.lexer.lineno += len(t.value)


# 10. Tratamento de erros
def t_error(t):
    print(
        f"Caractere inválido: {t.value[0]} "
        f"na linha {t.lineno}"
    )

    t.lexer.skip(1)


# 11. Criar o analisador léxico
def criar_lexer():
    return lex.lex()
