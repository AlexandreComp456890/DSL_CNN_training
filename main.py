
"""Ponto de entrada da DSL para treinamento de CNNs."""

import sys
from pathlib import Path
from pprint import pprint

from Language.lexer import criar_lexer
from Language.parser import criar_parser


def main():
    # Caminho padrao do exemplo
    caminho = (
        Path(__file__).resolve().parent
        / "Code"
        / "mnist.dsl"
    )

    # Permite informar outro arquivo pelo terminal
    if len(sys.argv) > 1:
        caminho = Path(sys.argv[1])

    # Leitura do codigo-fonte
    codigo = caminho.read_text(encoding="utf-8")

    # Criacao dos analisadores
    lexer = criar_lexer()
    parser = criar_parser()

    # Analise do codigo
    resultado = parser.parse(
        codigo,
        lexer=lexer
    )

    # Exibicao da arvore sintatica
    print("Analise sintatica realizada com sucesso!")
    pprint(resultado)


if __name__ == "__main__":
    main()
