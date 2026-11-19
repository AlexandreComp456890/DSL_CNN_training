# Definicao do dataset
DATASET MNIST;

# Divisao dos dados
SPLIT train=0.8 validation=0.2 seed=42;

# Pre-processamento
NORMALIZE mode=zero_one;

# Definicao da rede neural
MODEL CNN {

    # Primeira camada convolucional
    CONV filters=32 kernel=3;
    RELU;
    POOL size=2;

    # Segunda camada convolucional
    CONV filters=64 kernel=3;
    RELU;
    POOL size=2;

    # Conversao para vetor
    FLATTEN;

    # Camadas totalmente conectadas
    DENSE units=128;
    RELU;

    # Regularizacao
    DROPOUT rate=0.5;

    # Camada de saida
    DENSE units=10;
}

# Configuracao do treinamento
TRAIN epochs=10 batch=32 optimizer=adam lr=0.001;

# Avaliacao do modelo
EVALUATE test;

# Salvamento do modelo
SAVE "outputs/modelo_mnist.pt";
