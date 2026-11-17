from pathlib import Path
from Language.lexer import criar_lexer

# Caminho para o arquivo da DSL
caminho = (
    Path(__file__).resolve().parent
    / "Code"
    / "mnist.dsl"
)

# Ler o código-fonte
codigo = caminho.read_text(encoding="utf-8")

# Cria o analisador léxico
lexer = criar_lexer()

# Enviar o código para análise
lexer.input(codigo)

# Mostrar os tokens
for token in lexer:
    print(token.type, token.value)
