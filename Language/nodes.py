# Define as estruturas utilizadas para representar os comandos na árvore sintática abstrata (AST).
"""Define as estruturas da arvore sintatica abstrata (AST) da DSL."""
from dataclasses import dataclass
from typing import Any

@dataclass
class Comando:
    """Representa um comando da DSL e seus parametros."""

    nome: str                   # Nome do comando (DATASET, TRAIN, etc.)
    parametros: dict[str, Any]  # Parametros e seus respectivos valores

@dataclass
class Camada:
    """Representa uma camada da rede neural convolucional."""

    nome: str                   # Tipo da camada (CONV, RELU, POOL, etc.)
    parametros: dict[str, Any]  # Configuracoes especificas da camada

@dataclass
class Modelo:
    """Representa a arquitetura de um modelo de inteligencia artificial."""

    tipo: str                   # Tipo do modelo (CNN)
    camadas: list[Camada]       # Camadas que compoem a arquitetura

@dataclass
class Programa:
    """Representa o programa completo na arvore sintatica abstrata."""

    instrucoes: list[Comando | Modelo]  # Instrucoes reconhecidas pelo parser