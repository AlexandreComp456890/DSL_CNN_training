# Contém os testes responsáveis por validar as regras sintáticas da DSL.


"""Testes do analisador sintatico."""

import unittest

from Language.lexer import criar_lexer
from Language.parser import criar_parser


def analisar(codigo):
    return criar_parser().parse(
        codigo,
        lexer=criar_lexer()
    )


class TestParser(unittest.TestCase):

    def test_dataset_conhecido(self):
        programa = analisar("DATASET MNIST;")

        comando = programa.instrucoes[0]

        self.assertEqual(comando.nome, "DATASET")
        self.assertEqual(
            comando.parametros["valor"],
            "MNIST"
        )

    def test_dataset_diretorio(self):
        programa = analisar(
            'DATASET "datasets/animais";'
        )

        comando = programa.instrucoes[0]

        self.assertEqual(
            comando.parametros["tipo"],
            "diretorio"
        )

    def test_varios_comandos(self):
        programa = analisar(
            "DATASET MNIST; "
            "TRAIN epochs=10 batch=32;"
        )

        self.assertEqual(
            len(programa.instrucoes),
            2
        )

    def test_erro_sintatico(self):
        with self.assertRaises(SyntaxError):
            analisar("DATASET = MNIST;")

    def test_parametro_repetido(self):
        with self.assertRaises(ValueError):
            analisar(
                "TRAIN epochs=10 epochs=20;"
            )

    def test_modelo_cnn(self):
        programa = analisar(
            "MODEL CNN { "
            "CONV filters=32 kernel=3; "
            "RELU; "
            "FLATTEN; "
            "DENSE units=10; "
            "}"
        )

        modelo = programa.instrucoes[0]

        self.assertEqual(modelo.tipo, "CNN")
        self.assertEqual(len(modelo.camadas), 4)


if __name__ == "__main__":
    unittest.main()
